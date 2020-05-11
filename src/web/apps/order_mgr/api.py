# -*- coding: utf-8 -*-


import os
import re

from ..custom_views import APIView, APIException
from .. import code_msg
from utils import get_dt, make_dir
from flask import current_app, g
from werkzeug.datastructures import FileStorage
# from werkzeug.utils import secure_filename
from voluptuous import Schema, Required, Coerce, Optional, Any
from utils.args_schema_common import page_schema, only_num_id


class UploadOrder(APIView):

    _filter_null = True
    _schema = Schema({
        Required("mail_pd_id"): only_num_id,
        Required("receiver"): Coerce(str),
        Required("order_status"): Coerce(int),
        Required("order_id"): str,
        Optional("apply_time"): str,
        Optional("wangwang_id"): str,
        Optional("goods_id"): str,
        Optional("return_pd_id"): str,
        Optional("return_pd_company"): str,
        Optional("comment"): str,
        Optional("upload_order_img"): Any(FileStorage, str)
    })

    def post(self, request):
        args_map = request.req_args
        select_sql = """SELECT 1 FROM `tb_order_info` WHERE `mail_pd_id`=?"""
        if self.db.get_value(select_sql, (args_map["mail_pd_id"], )):
            raise APIException(code_msg.CODE_DATA_EXIST)
        insert_sql = """INSERT INTO `tb_order_info`(`mail_pd_id`, `receiver`, `order_status`, `order_id`, `apply_time`, `wangwang_id`,
         `goods_id`, `return_pd_company`, `return_pd_id`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        result = self.db.execute(insert_sql, (args_map["mail_pd_id"], args_map["receiver"], args_map["order_status"], args_map["order_id"],
                         args_map["apply_time"], args_map["wangwang_id"], args_map["goods_id"],
                         args_map["return_pd_company"], args_map["return_pd_id"]))
        img_id = result.lastrowid
        file_obj = args_map.get("upload_order_img")
        if file_obj:
            try:
                filename = self._upload_images(file_obj, img_id)
                self.db.execute("""UPDATE `tb_order_info` SET `img_name`=? WHERE `id`=?""", (filename, img_id))
            except:
                self.db.execute("""DELETE FROM tb_order_info WHERE `id`=?""", (img_id, ))
                if os.path.exists(self.upload_img_path):
                    os.remove(self.upload_img_path)
                raise APIException(code_msg.CODE_UPLOAD_ORDER_ERROR)

    def _upload_images(self, file_obj, img_id):
        filename = file_obj.filename
        file_extensions = filename.rsplit('.', 1)[1]
        if '.' not in filename and file_extensions not in current_app.config["ALLOWED_IMG_EXTENSIONS"]:
            raise APIException(code_msg.CODE_UPLOAD_ORDER_ERROR)
        self.upload_img_path = os.path.join(make_dir(current_app.config["UPLOAD_IMG_PATH"]), str(img_id)+"."+file_extensions)
        file_obj.save(self.upload_img_path)
        return filename


class ListOrderContent(APIView):

    _schema = Schema({
        **page_schema,
        Optional("recycle"): str,
        Optional("search_order"): Coerce(str)
    })
    _cn_regex = re.compile(r'[a-zA-Z\u4e00-\u9fa5]+')
    _isdigit_regex = re.compile(r'\d+')

    def get(self, request):
        cond, args = self._get_sql_cond_args(request)
        cnt_sql = """SELECT COUNT(*) FROM `tb_order_info` WHERE """ + cond
        sql_data = "SELECT `mail_pd_id`, `receiver`, `update_time` FROM `tb_order_info` WHERE " + cond + \
                   " ORDER BY `update_time` DESC" + request.page_info.limit_clause
        cnt = self.db.get_value(cnt_sql, args)
        query_result = self.db.get_all_row(sql_data, args)
        field_name = g.field_name
        if cnt:
            request.page_info.total = cnt
        result = [dict(zip(field_name, data)) for data in query_result]
        print(result)
        return result

    def _get_sql_cond_args(self, request):
        req_args = request.req_args
        if req_args.get("recycle"):
            is_delete = 1
        else:
            is_delete = 0
        search_order = req_args.get("search_order", "")
        if self._isdigit_regex.match(search_order):
            cond = "`is_delete`=? AND `mail_pd_id` LIKE ?"
            args = (is_delete, "%"+search_order+"%")
        elif self._cn_regex.match(search_order):
            cond = "`is_delete`=? AND `receiver` LIKE ?"
            args = (is_delete, "%"+search_order+"%")
        else:
            cond = "`is_delete`=?"
            args = (is_delete, )
        return cond, args


class UpdateOrder(APIView):
    pass


class RemoveOrder(APIView):

    _schema = Schema({
        Required("mail_pd_id"): only_num_id,
        Required("status"): int
    })

    def post(self, request):
        dt = get_dt()
        status = request.req_args.get("status")
        mail_pd_id = request.req_args.get("mail_pd_id")
        update_sql = """UPDATE `tb_order_info` SET `is_delete`=?, `update_time`=? WHERE `mail_pd_id`=?"""
        if status == 1:  # 恢复
            self.db.execute(update_sql, (0, dt, mail_pd_id))
        elif status == 2:  # 彻底删除
            id, img_name = self.db.get_one_row("""select `id`, `img_name` from tb_order_info WHERE `mail_pd_id`=?""", (mail_pd_id, ))
            if img_name:
                filename = str(id) + "." + img_name.rsplit('.', 1)[1]
                img_path = os.path.join(current_app.config["UPLOAD_IMG_PATH"], filename)
                if os.path.exists(img_path):
                    os.remove(img_path)
            self.db.execute("""DELETE FROM tb_order_info WHERE `mail_pd_id`=?""", (mail_pd_id, ))

        elif status == 0:  # 逻辑删除
            self.db.execute(update_sql, (1, dt, mail_pd_id))
        else:
            raise APIException(code_msg.CODE_INVALID_ARGUEMNTS)
