# -*- coding: utf-8 -*-

import re


CODE_SUCC = 0 #
CODE_INVALID_ARGUEMNTS = 400 # 参数错误
CODE_PERMISSION_DENIED = 403 # 没有该操作的权限
CODE_OBJ_NOT_FOUND = 404 # 记录不存在
CODE_NOT_LOGIN = 401 # 登录已失效，请重新登录
CODE_MTH_NOT_ALLOWED = 405 # 不允许使用该HTTP方法


_CODE_MSG_MAP = dict()
_reg = re.compile(r'^CODE.*?=\s*(\d+)\s*(?:\#\s*(.*?))?\s*$')
def _load_all():
    with open(__file__, encoding='utf8') as f:
        for line in f:
            line = line.strip()
            res = _reg.match(line)
            if not res:
                continue
            code, msg = res.groups()
            _CODE_MSG_MAP[int(code)] = (msg or '')
_load_all()

def get_msg(code):
    return _CODE_MSG_MAP.get(code, '')

if __name__ == '__main__':
    print(_CODE_MSG_MAP)
