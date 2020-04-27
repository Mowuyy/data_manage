# -*- coding: utf-8 -*-

import logging

from flask import request
from flask_login import current_user

from . import get_remote_addr


class RequestLogFormatter(logging.Formatter):

    def format(self, record):
        record.url=request.url
        record.remote_addr = get_remote_addr()
        try:
            record.user_id = current_user.get_id()
        except:
            record.user_id = None
        return super().format(record)

