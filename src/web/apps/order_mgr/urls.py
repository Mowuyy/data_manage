# -*- coding: utf-8 -*-

from . import app
from .api import OrderUpload


app.add_url_rule("/order_upload", view_func=OrderUpload.as_view("order_upload"), methods=("POST", ))
