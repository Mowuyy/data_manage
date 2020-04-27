# -*- coding: utf-8 -*-

# from flask_login import current_user, AnonymousUserMixin
from flask import render_template


def error_403(e):
    # if isinstance(current_user._get_current_object(), AnonymousUserMixin):
    #     return "<h1>NOT FOUND</h1>"
    return render_template('403.html')


def error_404(e):
    # if isinstance(current_user._get_current_object(), AnonymousUserMixin):
    #     return "<h1>NOT FOUND</h1>"
    return render_template('404.html')


def init(app):
    app.register_error_handler(403, error_403)
    app.register_error_handler(404, error_404)
