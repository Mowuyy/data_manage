# -*- coding: utf-8 -*-

from flask import Blueprint


index = Blueprint('index', __name__, static_folder='../../static', template_folder='../../templates')

from . import views
