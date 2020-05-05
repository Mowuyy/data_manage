# -*- coding: utf-8 -*-

import os
import logging

import flask


class Config:
    SECRET_KEY = 's@d343$##f8Ks!@ND0ar1@!dkk02fAF'

    # 配置日志
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    LOG_LEVEL = logging.INFO
    LOGGER_NAME = 'web'
    from utils.log_formatter import RequestLogFormatter
    LOG_FORMATTER = RequestLogFormatter('%(asctime)s [%(levelname)s] %(pathname)s(%(lineno)d) %(remote_addr)s user(%(user_id)s): %(message)s')
    LOG_FILE_PATH = os.path.join(BASE_PATH, 'log/web.log')
    from logging.handlers import RotatingFileHandler
    from logging import StreamHandler
    FILE_HANDLER = RotatingFileHandler(filename=LOG_FILE_PATH, maxBytes=512*1024*1024, backupCount=20)
    CONSOLE_HANDLER = StreamHandler(flask.logging.wsgi_errors_stream)
    LOG_HANDLERS = []

    # 最大分页大小
    MAX_PAGE_SIZE = 150

    # 上传图片
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'}
    UPLOAD_DIR = "upload/images"

    @staticmethod
    def init_app(app:flask.Flask):
        app.debug = app.config.get('DEBUG', True)
        app.logger.name = app.config['LOGGER_NAME']
        app.logger.setLevel(app.config['LOG_LEVEL'])
        HANDLERS = app.config['LOG_HANDLERS']
        if HANDLERS:
            app.logger.handlers.clear()
            for handler in HANDLERS:
                handler.setFormatter(app.config['LOG_FORMATTER'])
                app.logger.addHandler(handler)

    @staticmethod
    def init_db(app: flask.Flask, db_url):

        @app.before_request
        def connect_db():
            from utils.db_utils import CustomDB
            app.db = CustomDB(db_url)

        @app.teardown_appcontext
        def shutdown_session(response_or_exc):
            from flask import current_app
            db = current_app.db
            if db is not None:
                db.close()
            return response_or_exc


class DevelopmentConfig(Config):
    """开发模式"""
    DEBUG = True

    DB_URL = "./db/data_mgr.db"

    #日志配置
    LOG_LEVEL = logging.DEBUG
    LOG_HANDLERS = [Config.FILE_HANDLER, Config.CONSOLE_HANDLER]


class ProductionConfig(Config):
    """生产模式"""
    DEBUG = False

    DB_URL = "./db/data_mgr.db"

    # 日志配置
    LOG_FILE_PATH = '/var/log/data_manage/web/web.log'
    from logging.handlers import RotatingFileHandler
    try:
        FILE_HANDLER = RotatingFileHandler(filename=LOG_FILE_PATH, maxBytes=512 * 1024 * 1024, backupCount=20)
        LOG_HANDLERS = (FILE_HANDLER,)
    except:
        pass
    LOG_LEVEL = logging.INFO


class TestingConfig(DevelopmentConfig):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
