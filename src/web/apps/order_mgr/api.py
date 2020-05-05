# -*- coding: utf-8 -*-


import os

from ..custom_views import APIView, APIException
from .. import code_msg
from utils import get_dt
from flask import current_app, g
from werkzeug.utils import secure_filename
from voluptuous import Schema, Required


class UploadOrder(APIView):

    _filter_null = True

    def post(self, request):
        # self._upload_images(request)
        args_map = request.req_args
        select_sql = """SELECT 1 FROM `tb_order_info` WHERE `order_id`=?"""
        if self.db.get_value(select_sql, (args_map["order_id"], )):
            raise APIException(code_msg.CODE_DATA_EXIST)
        insert_sql = """INSERT INTO `tb_order_info`(`receiver`, `order_status`, `order_id`, `apply_time`, `wangwang_id`,
         `goods_id`, `mail_pd_id`, `return_pd_company`, `return_pd_id`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        self.db.execute(insert_sql, (args_map["receiver"], args_map["order_status"], args_map["order_id"],
                         args_map["apply_time"], args_map["wangwang_id"], args_map["goods_id"],
                         args_map["mail_pd_id"], args_map["return_pd_company"], args_map["return_pd_id"]))

    def _upload_images(self, request):
        file_dir = os.path.join(current_app.config["BASE_PATH"], current_app.config['UPLOAD_DIR'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files["file"]
        print(f.filename)
        # if f and allowed_file(f.filename):
        #     fname = secure_filename(f.filename)
        #
        #     ext = fname.rsplit('.', 1)[1]
        #     new_filename = Pic_str().create_uuid() + '.' + ext
        #     f.save(os.path.join(file_dir, new_filename))


class ListOrder(APIView):

    def get(self, request):
        sql = "SELECT * FROM `tb_order_info` WHERE `is_delete`=0 ORDER BY `id` DESC" + request.page_info.limit_clause
        query_result = self.db.get_all_row(sql)
        field_name = g.field_name
        del field_name[0]
        del field_name[11:]
        result = list()
        for data in query_result:
            data = list(data)
            del data[0]
            del data[11:]
            result.append(dict(zip(field_name, data)))
        return result


class RemoveOrder(APIView):

    def post(self, request):
        dt = get_dt()
        order_id = request.req_args.get("order_id")
        sql = """UPDATE `tb_order_info` SET `is_delete`=1, `update_time`=? WHERE `order_id`=?"""
        self.db.execute(sql, (dt, order_id))


class DetailOrder(APIView):

    def get(self, request):
        order_id = request.req_args.get("order_id")
        sql = """SELECT * FROM tb_order_info WHERE order_id=? AND is_delete=0"""
        query_result = list(self.db.get_one_row(sql, (order_id, )))
        field_name = g.field_name
        del field_name[0]
        del field_name[11:]
        del query_result[0]
        del query_result[11:]
        return dict(zip(field_name, query_result))
