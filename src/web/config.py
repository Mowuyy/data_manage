# -*- coding: utf-8 -*-

import os
import logging

import flask


class Config:
    SECRET_KEY = 's@d343$##f8Ks!@ND0ar1@!dkk02fAF'

    # 自动commit提交到数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 配置日志
    LOG_LEVEL = logging.INFO
    LOGGER_NAME = 'web'
    from utils.log_formatter import RequestLogFormatter
    LOG_FORMATTER = RequestLogFormatter('%(asctime)s [%(levelname)s] %(pathname)s(%(lineno)d) %(remote_addr)s user(%(user_id)s): %(message)s')
    LOG_FILE_PATH = 'log/web.log'
    from logging.handlers import RotatingFileHandler
    from logging import StreamHandler
    FILE_HANDLER = RotatingFileHandler(filename=LOG_FILE_PATH, maxBytes=512*1024*1024, backupCount=20)
    CONSOLE_HANDLER = StreamHandler(flask.logging.wsgi_errors_stream)
    LOG_HANDLERS = []

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


class DevelopmentConfig(Config):
    """开发模式"""
    DEBUG = True

    # 连接 mysql URl 设置
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                           'mysql://127.0.0.1:3306/order_manage?user=order_manage&password=order_manage$,.123'

    #日志配置
    LOG_LEVEL = logging.DEBUG
    LOG_HANDLERS = [Config.FILE_HANDLER, Config.CONSOLE_HANDLER]


class ProductionConfig(Config):
    """生产模式"""
    DEBUG = False

    # 连接 mysql URl 设置
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                           'mysql://127.0.0.1:3306/order_manage?user=order_manage&password=order_manage$,.123'

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
