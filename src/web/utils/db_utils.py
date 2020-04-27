# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy.util import safe_reraise


class SQLAlchemy(_SQLAlchemy):

    def get_one_row(self, sql, *args, **kwargs):
        res = self.execute(sql, *args, **kwargs)
        return res.fetchone()

    def execute(self, sql, *args, **kwargs):
        return self.session.connection().execute(sql, *args, **kwargs)

    def get_value(self, sql, *args, default=None, **kwargs):
        res = self.execute(sql, *args, **kwargs)
        if res.rowcount:
            return res.fetchone()[0]
        return default

    def begin(self):
        return self.session.begin()

    def commit(self):
        return self.session.commit()

    def rollback(self):
        return self.session.rollback()

    def transaction(self, func, *args, **kwargs):
        self.commit()
        try:
            rtn = func(self.session.connection(), *args, **kwargs)
            self.commit()
            return rtn
        except:
            with safe_reraise():
                self.rollback()
