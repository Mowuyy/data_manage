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

    def get_one_row(self, sql, *args, **kwargs):
        ret = self.execute(sql, *args, **kwargs)
        g.field_name = self.get_field_name(ret)
        return self.cursor.fetchone()

    def get_last_row(self, sql, *args, **kwargs):
        ret = self.execute(sql, *args, **kwargs)
        g.field_name = self.get_field_name(ret)
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
