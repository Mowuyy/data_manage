// 订单上传
function orderSubmitSuccess() {
    alert("订单上传成功！");
    $("#upload_order_form input").val("");
}

function orderSubmit() {
    var formData = {};
    var formDataArr = $("#upload_order_form").serializeArray();
    $.each(formDataArr, function (i, item) {
        formData[item.name] = item.value;
    });
    postRequest("/order_mgr/upload_order", formData, orderSubmitSuccess);
}


// 订单列表页
function showOrder(page) {
    getRequest("/order_mgr/list_order", {"page": page || 1, "page_size": pageInfo.pageSize}, showOrderSuccess);
}

function showOrderSuccess(result) {
    var data = result.data.items;
    if (data.length == 0) {
        $(".body_right").empty().html("<h1 style='text-align: center;margin-top: 200px;font-size: 20px;color: #999;'>无数据，请您先上传订单信息</h1>");
        return;
    }
    $(".body_right").empty().html("<div class='page_content'></div><div class='page_flag'></div>");
    $(".page_flag").css({"margin-top": "50px", "text-align": "center"});
    $(".page_content").append(
        '<div id="search_id" style="margin-left: 120px;margin-top: 50px;">' +
        '<input name="" type="text" placeholder="请输入订单号或收件人" style="margin-right: 20px;width:200px;height: 25px;border:0.5px solid #378888">' +
        '<a href="javascript:void(0);" data-type="reload" onclick="searchOrder()"><img src="/static/images/ser-icon.jpg"></a></div>' +
        '<table><tr style="font-size: 20px;color: #3a3e50;"><th>订单号</th><th>收件人</th><th>上传时间</th><th>操作</th></tr></table>');
        for (var i=0; i<data.length; i++) {
            $(".page_content"+ " table").append(
                "<tr style='font-size: 16px;color: #999'><td>" + data[i].order_id + "</td>" +
                "<td>" + data[i].receiver + "</td>" +
                "<td>" + data[i].update_time + "</td>" +
                "<td><a style='color: #999;' href='/order_mgr/order_detail/" + data[i].order_id + "' target='_blank'>详情</a> | " +
                    "<a style='color: #999' href='javascript:;' onclick='removeDetail(" + data[i].order_id + ")'>删除</a></td>" +
                "</tr>");
        }
    $(".page_content th, .page_content td").css({
        "width": "10%",
        "text-align": "center",
        "padding-top": "20px"
    });
    pageAction(".page_flag", showOrder, result.data.total, result.data.page);
}

// 搜索框
function searchOrder(page, status) {
    var orderInfo = $("#search_id >input").val();
    var url = "/order_mgr/list_order";
    var data = {"page": page || 1, "page_size": pageInfo.pageSize, "search_order": orderInfo};
    if (status == 1) {
        // 订单回收站
        data["recycle"] = 1;
        getRequest(url, data, showRecycleOrderSuccess);
    } else {
        // 订单页
        getRequest(url, data, showOrderSuccess);
    }
}


function removeDetail(orderId) {
    postRequest("/order_mgr/remove_order", {"order_id": orderId, "recycle": 0}, removeDetailSuccess);
}

function removeDetailSuccess() {
    alert("订单删除成功！");
    showOrder();
}


// 回收订单
function showRecycleOrder(page) {
    getRequest("/order_mgr/list_order", {"page": page || 1, "page_size": pageInfo.pageSize, "recycle": 1}, showRecycleOrderSuccess);
}

function showRecycleOrderSuccess(result) {
    var data = result.data.items;
    if (data.length == 0) {
        $(".body_right").empty().html("<h1 style='text-align: center;margin-top: 200px;font-size: 20px;color: #999;'>无订单数据删除！</h1>");
        return;
    }
    $(".body_right").empty().html("<div class='page_content'></div><div class='page_flag'></div>");
    $(".page_flag").css({"margin-top": "50px", "text-align": "center"});
    $(".page_content").append(
        '<div id="search_id" style="margin-left: 120px;margin-top: 50px;">' +
        '<input name="" type="text" placeholder="请输入订单号或收件人" style="margin-right: 20px;width:200px;height: 25px;border:0.5px solid #378888">' +
        '<a href="javascript:void(0);" data-type="reload" onclick="searchOrder(1, 1)"><img src="/static/images/ser-icon.jpg"></a></div>' +
        '<table><tr style="font-size: 20px;color: #3a3e50;"><th>订单号</th><th>收件人</th><th>上传时间</th><th>操作</th></tr></table>');
        for (var i=0; i<data.length; i++) {
            $(".page_content"+ " table").append(
                "<tr style='font-size: 16px;color: #999'><td>" + data[i].order_id + "</td>" +
                "<td>" + data[i].receiver + "</td>" +
                "<td>" + data[i].update_time + "</td>" +
                "<td><a style='color: #999;' href='javascript:;' onclick='recoverDeleteOrder(" + data[i].order_id + ", 1)'>恢复</a> | " +
                "<a style='color: #999' href='javascript:;' onclick='recoverDeleteOrder(" + data[i].order_id + ", 2)'>彻底删除</a></td>" +
                "</tr>");
        }
    $(".page_content th, .page_content td").css({
        "width": "10%",
        "text-align": "center",
        "padding-top": "20px"
    });
    pageAction(".page_flag", showRecycleOrder, result.data.total, result.data.page);
}

function recoverDeleteOrder(orderId, recycle) {
    postRequest("/order_mgr/remove_order", {"order_id": orderId, "recycle": recycle}, recoverDeleteOrderSuccess);
}

function recoverDeleteOrderSuccess() {
    alert("操作成功！");
    showRecycleOrder();
}
