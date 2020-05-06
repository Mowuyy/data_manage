# -*- coding: utf-8 -*-

from flask import Blueprint


app = Blueprint('order_mgr', __name__, static_folder='../../static', template_folder='../../templates')

from . import views
from . import urls
