# -*- coding: utf-8 -*-

from ..custom_views import APIView, APIException
from .. import code_msg
from voluptuous import Schema, Required


data_field = ("id", "receiver", "order_status", "order_id", "apply_time", "wangwang_id", "goods_id", "mail_pd_id",
              "return_pd_company", "return_pd_id", "comment", "update_time")

"""
`id`, `receiver`, `order_status, `order_id`, `apply_time`, `wangwang_id`, `goods_id`, `mail_pd_id`, `return_pd_company`, `return_pd_id`, `comment`, `update_time` 
"""

class UploadOrder(APIView):

    _schema = True
    _filter_null = True

    def post(self, request):
        args_map = request.req_args
        select_sql = """SELECT 1 FROM `tb_order_info` WHERE `order_id`=?;"""
        if self.db.get_value(select_sql, (args_map["order_id"], )):
            raise APIException(code_msg.CODE_DATA_EXIST)
        insert_sql = """INSERT INTO `tb_order_info`(`receiver`, `order_status`, `order_id`, `apply_time`, `wangwang_id`,
         `goods_id`, `mail_pd_id`, `return_pd_company`, `return_pd_id`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        self.db.execute(insert_sql, (args_map["receiver"], args_map["order_status"], args_map["order_id"],
                         args_map["apply_time"], args_map["wangwang_id"], args_map["goods_id"],
                         args_map["mail_pd_id"], args_map["return_pd_company"], args_map["return_pd_id"]))


class ListOrder(APIView):

    _schema = True

    def get(self, request):
        sql = "SELECT * FROM `tb_order_info` WHERE `is_delete`=0 ORDER BY `id` DESC" + request.page_info.limit_clause
        return self.db.get_all_row(sql)


class RemoveOrder(APIView):

    _schema = True

    def post(self, request):
        order_id = request.req_args.get("order_id")
        sql = """UPDATE `tb_order_info` SET `is_delete`=1 WHERE `order_id`=?"""
        self.db.execute(sql, (order_id, ))


class DetailOrder(APIView):

    _schema = True

    def get(self, request):
        order_id = request.req_args.get("order_id")
        sql = """SELECT * FROM tb_order_info WHERE order_id=? AND is_delete=0;"""
        return self.db.get_one_row(sql, (order_id, ))
