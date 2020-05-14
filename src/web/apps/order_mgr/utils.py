# -*- coding: utf-8 -*-

from voluptuous import Schema, Required, Coerce, Any, Optional
from werkzeug.datastructures import FileStorage
from utils.args_schema_common import only_num_id


order_schema = Schema({
    Required("mail_pd_id"): only_num_id,
    Required("receiver"): Coerce(str),
    Required("order_status"): Coerce(int),
    Required("order_id"): str,
    Optional("apply_time"): str,
    Optional("wangwang_id"): str,
    Optional("goods_id"): str,
    Optional("return_pd_id"): str,
    Optional("return_pd_company"): str,
    Optional("comment"): str,
    Optional("upload_order_img"): Any(FileStorage, str),
    Optional("action"): str
})


