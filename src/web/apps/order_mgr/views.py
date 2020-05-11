# -*- coding: utf-8 -*-

import os

from flask import render_template, current_app, g, make_response

from . import app


@app.route("/render_upload")
def order_mgr():
    return render_template("apps/order_upload.html")


@app.route("/order_list")
def order_list():
    return render_template("apps/order_list.html")


@app.route("/order_detail/<string:mail_pd_id>")
def order_detail(mail_pd_id):
    db = current_app.db
    query_result = list(db.get_one_row("""SELECT * FROM tb_order_info WHERE `mail_pd_id`=? AND `is_delete`=0""", (mail_pd_id, )))
    field_name = g.field_name
    del field_name[0]
    del field_name[11:]
    del query_result[0]
    del query_result[11:]
    query_result = map(lambda item: item if item else "空", query_result)
    data = dict(zip(field_name, query_result))
    order_status = {
        1: "退货",
        2: "退改",
        3: "丢件",
        4: "其他"
    }
    data.update({"order_status": order_status[data["order_status"]]})
    print(data)
    return render_template("apps/order_detail.html", data=data)


@app.route("/order_recycle")
def order_recycle():
    return render_template("apps/order_recycle_list.html")


@app.route("/img_detail/<string:mail_pd_id>")
def img_detail(mail_pd_id):
    if not (isinstance(mail_pd_id, str) or mail_pd_id):
        return render_template("404.html")
    db = current_app.db
    id, img_name = db.get_one_row("""select `id`, `img_name` from tb_order_info WHERE`mail_pd_id`=?""", (mail_pd_id, ))
    if img_name:
        filename = str(id) + "." + img_name.rsplit('.', 1)[1]
        img_path = os.path.join(current_app.config["UPLOAD_IMG_PATH"], filename)
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                response = make_response(f.read())
                response.headers['Content-Type'] = 'image/png'
                return response
