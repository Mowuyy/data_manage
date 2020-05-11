# -*- coding: utf-8 -*-

from flask import render_template, current_app, g

from . import app


@app.route("/render_upload")
def order_mgr():
    return render_template("apps/order_upload.html")


@app.route("/order_list")
def order_list():
    return render_template("apps/order_list.html")


@app.route("/order_detail/<string:order_id>")
def order_detail(order_id):
    db = current_app.db
    query_result = list(db.get_one_row("""SELECT * FROM tb_order_info WHERE order_id=? AND is_delete=0""", (order_id, )))
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
    return render_template("apps/order_detail.html", data=data)


@app.route("/order_recycle")
def order_recycle():
    return render_template("apps/order_recycle_list.html")
