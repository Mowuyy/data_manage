# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import *

from config import config
from utils.db_utils import SQLAlchemy


"""初始化各组件"""
db = SQLAlchemy(engine_options={"pool_recycle": 300, 'echo': False})

def create_app(config_name):
    app = Flask(__name__, static_url_path='/static', static_folder='../static')
    CORS(app, supports_credentials=True)
    config_obj = config[config_name]
    app.config.from_object(config_obj)
    app.config.from_pyfile('application.cfg', silent=True)
    config_obj.init_app(app)
    config_obj.init_db(app, config_obj.DB_URL)
    # login_manager.init_app(app)
    from .import error_pages
    error_pages.init(app)

    """ 按照功能模块来组织蓝图 """
    from .index import app as index_blueprint
    app.register_blueprint(index_blueprint, url_prefix='/')

    from .main import app as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/data_manage')

    from .order_mgr import app as order_mgr_blueprint
    app.register_blueprint(order_mgr_blueprint, url_prefix='/order_mgr')

    return app
