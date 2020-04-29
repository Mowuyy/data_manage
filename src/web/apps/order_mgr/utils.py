# -*- coding: utf-8 -*-

from flask import g


def build_order_data(data: list) -> dict:
    field_name = g.field_name
    del field_name[0]
    del field_name[11:]
    del data[0]
    del data[11:]
    return dict(zip(field_name, data))

