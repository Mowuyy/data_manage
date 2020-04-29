# -*- coding: utf-8 -*-

from ..custom_views import APIView, APIException
from .. import code_msg
from .utils import build_order_data
from voluptuous import Schema, Required


class UploadOrder(APIView):

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

    def get(self, request):
        sql = "SELECT * FROM `tb_order_info` WHERE `is_delete`=0 ORDER BY `id` DESC" + request.page_info.limit_clause
        query_result = self.db.get_all_row(sql)
        return [build_order_data(list(data)) for data in query_result]


class RemoveOrder(APIView):

    def post(self, request):
        order_id = request.req_args.get("order_id")
        sql = """UPDATE `tb_order_info` SET `is_delete`=1 WHERE `order_id`=?"""
        self.db.execute(sql, (order_id, ))


class DetailOrder(APIView):

    def get(self, request):
        order_id = request.req_args.get("order_id")
        sql = """SELECT * FROM tb_order_info WHERE order_id=? AND is_delete=0;"""
        query_result = self.db.get_one_row(sql, (order_id, ))
        return build_order_data(list(query_result))
