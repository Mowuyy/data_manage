# -*- coding: utf-8 -*-

import os
from pathlib import Path
from datetime import datetime

from flask import request

__all__ = [
    "get_dt",
    "get_remote_addr",
    "get_client_abbr",
    "get_client_logo_file"
]


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_dt():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_remote_addr():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


def get_client_abbr(db, client_id):
    return db.get_value('SELECT abbr FROM tb_client WHERE id=%s AND abbr IS NOT NULL', (client_id,), default='数据管理系统')


def get_client_logo_file(db, client_id):
    res = db.execute('SELECT logo_file FROM tb_client WHERE id=%s', (client_id,))
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), 'web/static')
    if res.rowcount:
        img = res.fetchone()[0]
        if img:
            path = os.path.join(base_path, 'client_logo_file')
            img_path = os.path.join(path, img)
            if Path(img_path).is_file():
                return os.path.join('/static', f'client_logo_file/{img}').replace('\\', '/')
    return os.path.join('/static', 'images/logo.png').replace('\\', '/')
