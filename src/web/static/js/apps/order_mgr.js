function orderSubmitSuccess(result) {
    alert("订单上传成功！");
    $("#upload_order_form input").val("");
}

function orderSubmit() {
    var formData = {};
    var formDataArr = $("#upload_order_form").serializeArray();
    $.each(formDataArr, function (i, item) {
        formData[item.name] = item.value;
    });
    postRequest("/order_mgr/upload_order", formData, orderSubmitSuccess)
}

function showOrder() {
    getRequest("/order_mgr/list_order", {"page": 1, "page_size": 10}, showOrderSuccess);
}

function showOrderSuccess(result) {
    var data = result.data.items;
    $(".body_right").empty();
    $(".body_right").append(
        '<table><tr style="font-size: 20px;color: #3a3e50;"><th>订单号</th><th>上传时间</th><th>操作</th></tr></table>');

    for (var i=0; i<data.length; i++) {
        $(".body_right table").append(
            "<tr style='font-size: 18px;color: #999'><td>" + data[i].order_id + "</td>" +
                "<td>" + data[i].update_time + "</td>" +
                "<td><a style='color: #999;' href='javascript:;' onclick='showDetail(" + data[i].order_id + ")'>详情</a> | " +
                    "<a style='color: #999' href='javascript:;' onclick='removeDetail(" + data[i].order_id + ")'>删除</a></td>" +
            "</tr>");
    }

    $(".body_right th, .body_right td").css({
        "width": "10%",
        "text-align": "center",
        "padding-top": "20px",
        // "padding-right": '100px'
    });

}

function showDetail(orderId) {
    getRequest("/order_mgr/detail_order", {"order_id": orderId}, showDetailSuccess)

}



function showDetailSuccess(result) {
    orderStatus = {1: "退货", 2: "退改", 3: "丢件", 4: "其他"};

    function filterNull(data) {
        if (data) {
            return data
        } else {
            return "空"
        }
    }

    $(".body_right").empty();
    $(".body_right").append(
        "<label>收件人: </label><span>" + filterNull(result.data.receiver) + "</span><br>" +
        "<label>订单编号: </label><span>" + filterNull(result.data.order_id)+ "</span><br>" +
        "<label>旺旺名称: </label><span>" + filterNull(result.data.wangwang_id) + "</span><br>" +
        "<label>订单状态: </label><span>" + filterNull(orderStatus[result.data.order_status]) + "</span><br>" +
        "<label>申请时间: </label><span>" + filterNull(result.data.apply_time) + "</span><br>" +
        "<label>产品型号: </label><span>" + filterNull(result.data.goods_id) + "</span><br>" +
        "<label>寄件物流单号: </label><span>" + filterNull(result.data.mail_pd_id) + "</span><br>" +
        "<label>退货物流公司: </label><span>" + filterNull(result.data.return_pd_company) + "</span><br>" +
        "<label>退货物流单号: </label><span>" + filterNull(result.data.return_pd_id) + "</span><br>" +
        "<label>备注: </label><span>" + filterNull(result.data.comment)
    );
    $(".body_right").css({
        "font-size": '18px',
        "color": '#999'
    });
    $(".body_right >label").css({
        "display": "inline-block",
        "width": "150px",
        "text-align": "right",
        "margin-right": '20px',
        "margin-left": '50px',
        "margin-top": '20px'
    })

}

function removeDetail(orderId) {
    postRequest("/order_mgr/remove_order", {"order_id": orderId}, removeDetailSuccess);
}

function removeDetailSuccess(result) {
    alert("订单删除成功！");
    showOrder();
}