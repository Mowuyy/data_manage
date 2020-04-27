# -*- coding: utf-8 -*-

from flask import render_template

from . import main


@main.route('/')
@main.route('/index')
def index():
    data = {
        "name": "老王",
        "age":  18,
        "order": 98347597234751203940123,
        "commodity": "摩托车脚垫"
    }
    return render_template("index.html", data=data)
