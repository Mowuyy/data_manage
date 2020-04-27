# -*- coding: utf-8 -*-

from flask import render_template

from . import main


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")
