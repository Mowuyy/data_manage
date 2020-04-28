# -*- coding: utf-8 -*-

from flask import url_for, redirect
from . import app


@app.route('/')
def index():
    return redirect(url_for('main.index'))
