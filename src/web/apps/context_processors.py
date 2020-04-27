# -*- coding: utf-8 -*-

from flask_login import current_user
# from . import db
from utils import get_client_abbr, get_client_logo_file


def has_perm(perm_tag):
    return current_user.can(perm_tag)


def is_module_open(module):
    return current_user.is_module_open(module)


def get_client_title():
    return get_client_abbr(db, current_user.client_id)


def get_client_img_path():
    return get_client_logo_file(db, current_user.client_id)


def init(app):
    app.jinja_env.globals['get_client_title'] = get_client_title
    app.jinja_env.globals['get_client_img_path'] = get_client_img_path

    app.jinja_env.globals['has_perm'] = has_perm
    app.jinja_env.globals['module_open'] = is_module_open


