# -*- coding: utf-8 -*-
import sqlite3

from werkzeug.wrappers.response import Response
from flask.views import View
import voluptuous
from flask.globals import request
import json, datetime, uuid, decimal
from types import GeneratorType
from . import code_msg
from flask_login import current_user
from flask import current_app


def check_login():
    if request.method == 'OPTIONS':
        return True
    elif current_app.login_manager._login_disabled:
        return True
    elif not current_user.is_authenticated:
        return False
        # return current_app.login_manager.unauthorized()
    return True

class PageInfo(object):

    def __init__(self, page, page_sz, total=0):
        self.page = page
        self.page_sz = page_sz
        self.offset = (page - 1) * page_sz
        self.total = total
        self.limit_clause = ' LIMIT %s OFFSET %s' % (page_sz, self.offset)


class Schema(voluptuous.Schema):
    def __init__(self, *args, extra=voluptuous.REMOVE_EXTRA, **kwargs):
        super(Schema, self).__init__(*args, extra=extra, **kwargs)


class CustomView(View):

    _schema:voluptuous.Schema = None
    auto_process_page = True
    _filter_null = False
    _perms = None
    _load_perms = True
    _login_required = True
    _need_module = None

    # def _check_perm(self):
    #     if not self._perms:
    #         return True
    #     return current_user.can(self._perms, self._load_perms)
    #
    # def _check_module_open(self):
    #     if not self._need_module:
    #         return True
    #     return current_user.is_module_open(self._need_module)

    def _check_login(self):
        if self._login_required and not check_login():
            return False
        return True

    def _check_can_access(self):
        if not self._check_login():
            current_app.logger.warn('url="%s", login required', request.url)
            return self._on_login_check_failed()
        # if not self._check_perm():
        #     current_app.logger.warn('url="%s", permission denied', request.url)
        #     return self._on_403()
        # if not self._check_module_open():
        #     current_app.logger.warn('url="%s", module not open', request.url)
        #     return self._on_module_not_open()
        return None
#
    def dispatch_request(self, *args, **kwargs):
        method = getattr(self, request.method.lower(), None)
        if method is None and request.method == 'HEAD':
            method = getattr(self, 'get', None)
        if method is None:
            current_app.logger.warn('url="%s", method="%s"', request.url, method)
            return self._on_405()

        # 验证权限
        # rtn = self._check_can_access()
        # if rtn:
        #     return rtn
        auto_process_page = False
        all_req_args = None
        if self._schema:
            try:
                # 获取参数
                req_args = request.args.to_dict()
                if request.json:
                    req_args.update(request.json)
                if request.values:
                    req_args.update(request.values)
                if request.files:
                    req_args.update(request.files)

                print(req_args)
                # 参数校验
                req_args = self._schema(req_args)

                if self._filter_null:
                    req_args = {k: v if v else None for k, v in req_args.items()}

                # 分页处理
                if self.auto_process_page and "page" in req_args:
                    page_sz = int(req_args.pop('page_size'))
                    if not 1 <= page_sz <= current_app.config['MAX_PAGE_SIZE']:
                        current_app.logger.warn('url="%s", page size over max', request.url)
                        return self._on_argument_invalid(ValueError('invalid page size'))
                    page = int(req_args.pop('page'))
                    request.page_info = PageInfo(page, page_sz)
                    auto_process_page = True
                request.req_args = req_args

                # 获取db连接
                self.db = current_app.db
            except voluptuous.MultipleInvalid as e:
                current_app.logger.warn('request invalid, url="%s", args="%s", exc="%s"', request.url, all_req_args, e)
                return self._on_argument_invalid(e)
        try:
            self.pre_check(request)
            return self._packet_response(method(request, *args, **kwargs), (request.page_info if auto_process_page else None))
        except Exception as e:
            return self._on_exception(e)
#
    def _packet_response(self, rtn, page_info:PageInfo):
        return rtn
#
    def _on_argument_invalid(self, e):
        return Response('<h1>Invalid Request</h1>', content_type='text/html')
#
    def _on_405(self):
        return Response('<h1>Method Not Allowed!!!</h1', content_type='text/html')
    def _on_exception(self, e):
        raise

    def pre_check(self, request):
        pass

    def _on_login_check_failed(self):
        return current_app.login_manager.unauthorized()


class _JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return datetime.date.strftime(o, '%Y-%m-%d')
        elif isinstance(o, datetime.time):
            return datetime.time.strftime(o, '%H:%M:%S')
        elif isinstance(o, (uuid.UUID, )):
            return str(o)
        elif isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, GeneratorType):
            return tuple(o)
        else:
            return super(_JSONEncoder, self).default(o)

def to_resp_json(o):
    return json.dumps(o, ensure_ascii=False, cls=_JSONEncoder)

class APIResponse(Response):
    def __init__(self, data=None, code=code_msg.CODE_SUCC, msg=None, headers=None):
        if not msg:
            msg = code_msg.get_msg(code)
        super(APIResponse, self).__init__(to_resp_json({"code": code, "msg": msg, "data": data}), status=200, headers=headers,
                                          content_type='application/json; charset=utf-8')

class APIException(Exception):

    def __init__(self, code, msg=None, data=None):
        self.resp = APIResponse(data, code, msg)

class APIView(CustomView):

    _load_perms = False

    def _on_405(self):
        return APIResponse(code=code_msg.CODE_MTH_NOT_ALLOWED)

    def _on_403(self):
        return APIResponse(code=code_msg.CODE_PERMISSION_DENIED)

    def _packet_response(self, rtn, page_info):
        if isinstance(rtn, Response):
            return rtn
        if rtn is None:
            return APIResponse()
        if isinstance(rtn, int):
            return APIResponse(code=rtn)
        if page_info:
            return APIResponse({"page": page_info.page, "total": page_info.total, 'items': rtn})
        return APIResponse(rtn)

    def _on_argument_invalid(self, e):
        return APIResponse(code=code_msg.CODE_INVALID_ARGUEMNTS)

    def _on_exception(self, e):
        if isinstance(e, APIException):
            return e.resp
        raise

    def _on_login_check_failed(self):
        return APIResponse(code=code_msg.CODE_NOT_LOGIN)
