# -*- coding: utf-8 -*-

from flask import Blueprint


app = Blueprint('main', __name__, static_folder='../../static',template_folder='../../templates')

from . import views
