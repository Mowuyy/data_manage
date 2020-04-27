# -*- coding: utf-8 -*-
from flask import Blueprint


order_mgr = Blueprint('order_mgr', __name__, static_folder='../../static',template_folder='../../templates')

from . import urls, views
