# -*- coding: utf-8 -*-

from . import app
from .api import UploadOrder, ListOrder, RemoveOrder


app.add_url_rule("/upload_order", view_func=UploadOrder.as_view("upload_order"), methods=("POST", ))
app.add_url_rule("/list_order", view_func=ListOrder.as_view("list_order"), methods=("GET", ))
app.add_url_rule("/remove_order", view_func=RemoveOrder.as_view("remove_order"), methods=("POST", ))

