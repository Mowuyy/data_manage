# -*- coding: utf-8 -*-

from flask import render_template

from . import app


@app.route("/")
def order_mgr():
    return render_template("order_upload.html")
