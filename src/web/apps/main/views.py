# -*- coding: utf-8 -*-

from flask import render_template

from . import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("apps/index.html")
