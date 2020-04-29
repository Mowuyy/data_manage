# -*- coding: utf-8 -*-

import sqlite3

from flask import current_app, g

from apps.code_msg import CODE_DB_ROLLBACK
from apps.custom_views import APIException


class CustomDB(object):

    def __init__(self, db_url):
        self.cnn = sqlite3.connect(db_url, check_same_thread=False)
        self.cursor = self.cnn.cursor()

    def execute(self, sql, *args, **kwargs):
        try:
            result = self.cursor.execute(sql, *args, **kwargs)
            if sql.lower().startswith("select"):
                return result
            self.cnn.commit()
            return result
        except Exception as e:
            current_app.logger.warn(e)
            self.cnn.rollback()
            raise APIException(CODE_DB_ROLLBACK)

    def get_one_row(self, sql, *args, field=False, **kwargs):
        ret = self.execute(sql, *args, **kwargs)
        g.field_name = self.get_field_name(ret)
        return self.cursor.fetchone()

    def get_last_row(self, sql, *args, **kwargs):
        self.execute(sql, *args, **kwargs)
        result = self.cursor.fetchall()
        if result:
            return result[-1]

    def get_all_row(self, sql, *args, **kwargs):
        ret = self.execute(sql, *args, **kwargs)
        g.field_name = self.get_field_name(ret)
        return self.cursor.fetchall()

    def get_value(self, sql, *args, **kwargs):
        self.execute(sql, *args, **kwargs)
        result = self.cursor.fetchone()
        if result:
            return result[0]

    def get_field_name(self, ret):
        return list(map(lambda item: item[0], ret.description))

    def close(self):
        self.cursor.close()
        self.cnn.close()


if __name__ == '__main__':

    db = CustomDB("../db/data_mgr.db")
    # res = db.execute("insert into order_info(id, receiver, order_status) VALUES (?, ?, ?)", (3, "黎明", 1))
    # res = db.cursor.fetchone()
    # res = db.get_value("select id from order_info ORDER BY id DESC;")
    res = db.get_all_row("select * from tb_order_info WHERE is_delete=0;")

    # select_sql = """SELECT 1 FROM order_info WHERE receiver=? AND order_number=?;"""
    # res = db.get_value(select_sql, ("老王", 547))

    print(res)

    db.close()

