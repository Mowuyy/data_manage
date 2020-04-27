# -*- coding: utf-8 -*-

from flask import render_template

from . import order_mgr


@order_mgr.route("order_import")
def order_mgr():
    return render_template("order_import.html")
