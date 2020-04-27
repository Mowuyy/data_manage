# -*- coding: utf-8 -*-

from flask import Flask
# from flask_cors import *
# from flask_wtf.csrf import CSRFProtect

from config import config
# from utils.db_utils import SQLAlchemy


"""初始化各组件"""
# csrf = CSRFProtect()
# db = SQLAlchemy(engine_options={"pool_recycle": 300, 'echo': False})


def create_app(config_name):
    app = Flask(__name__, static_url_path='/static', static_folder='../static')
    # CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('application.cfg', silent=True)
    config[config_name].init_app(app)
    # csrf.init_app(app)
    # db.init_app(app)
    # login_manager.init_app(app)
    # from . import context_processors
    # context_processors.init(app)
    from .import error_pages
    error_pages.init(app)

    """ 按照功能模块来组织蓝图 """
    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint, url_prefix='/')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/data_manage')

    return app
