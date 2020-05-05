# -*- coding: utf-8 -*-

from flask import render_template

from . import app


@app.route("/render_upload")
def order_mgr():
    return render_template("apps/order_upload.html")
