# -*- coding: utf-8 -*-


import os
import re

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

    _cn_regex = re.compile(r'[a-zA-Z\u4e00-\u9fa5]+')
    _isdigit_regex = re.compile(r'\d+')

    def get(self, request):
        data_cond, data_args = self._get_sql_cond_args(request)
        sql_data = "SELECT `receiver`, `order_id`, `update_time` FROM `tb_order_info` WHERE " + data_cond + \
                   " ORDER BY `update_time` DESC" + request.page_info.limit_clause
        query_result = self.db.get_all_row(sql_data, data_args)
        field_name = g.field_name
        cnt = len(query_result)
        if cnt:
            request.page_info.total = cnt
        return [dict(zip(field_name, data)) for data in query_result]

    def _get_sql_cond_args(self, request):
        req_args = request.req_args
        if req_args.get("recycle"):
            is_delete = 1
        else:
            is_delete = 0
        search_order = req_args.get("search_order", "")
        if self._isdigit_regex.match(search_order):
            data_cond = "`is_delete`=? AND `order_id` LIKE ?"
            data_args = (is_delete, "%"+search_order+"%")
        elif self._cn_regex.match(search_order):
            data_cond = "`is_delete`=? AND `receiver` LIKE ?"
            data_args = (is_delete, "%"+search_order+"%")
        else:
            data_cond = "`is_delete`=?"
            data_args = (is_delete, )
        return data_cond, data_args


class RemoveOrder(APIView):

    def post(self, request):
        dt = get_dt()
        try:
            recycle = int(request.req_args.get("recycle"))
        except:
            raise APIException(code_msg.CODE_INVALID_ARGUEMNTS)
        order_id = request.req_args.get("order_id")
        update_sql = """UPDATE `tb_order_info` SET `is_delete`=?, `update_time`=? WHERE `order_id`=?"""
        if recycle == 1:  # 恢复
            self.db.execute(update_sql, (0, dt, order_id))
        elif recycle == 2:  # 彻底删除
            self.db.execute("""DELETE FROM tb_order_info WHERE `order_id`=?""", (order_id, ))
        elif recycle == 0:  # 逻辑删除
            self.db.execute(update_sql, (1, dt, order_id))
        else:
            raise APIException(code_msg.CODE_INVALID_ARGUEMNTS)
