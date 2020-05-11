var order_list_url = "/order_mgr/list_order_content";

// 删除、恢复、彻底删除
function removeOrderCommon(mail_pd_id, status, callBack) {
    var data = {"mail_pd_id": mail_pd_id, "status": status};
    postRequest("/order_mgr/remove_order", data, callBack);
}

// 订单通用搜索
function searchOrderCommon(page, status, callBack) {
    var orderInfo = $("#search_id >input").val();
    if (orderInfo.length <= 0) {
        alert("输入内容为空");
        return;
    }
    var data = {"page": page || 1, "page_size": pageInfo.pageSize, "search_order": orderInfo};
    if (status == 1) {
        data["recycle"] = 1;
        getRequest(order_list_url, data, callBack);
    } else {
        getRequest(order_list_url, data, callBack);
    }
}

// 订单内容
function orderContent(result, recycle, pageCallBack, nullContent) {
    var data = result.data.items;
    if (data.length == 0) {
        $(".body_right").empty().append("<h1>" + nullContent + "</h1>");
        return;
    }
    var content = "";
    content += '<div id="search_id">';
    content += '<input name="" type="text" placeholder="请输入订单号或收件人">';
    content += '<a href="javascript:void(0);" data-type="reload" onclick="searchOrder()"><img src="/static/images/ser-icon01.png"></a>';
    content += '</div>';
    content += '<table class="order_list_table">';
    content += '<tr><th>寄件物流单号</th><th>收件人</th><th>上传时间</th><th>操作</th></tr>';
    for (var i=0; i<data.length; i++) {
        var mail_pd_id= data[i].mail_pd_id;
        content += "<tr><td>" + mail_pd_id + "</td>";
        content += "<td>" + data[i].receiver + "</td>";
        content += "<td>" + data[i].update_time + "</td>";
        if (recycle) {
            content += "<td><a href='javascript:;' onclick='removeOrderRecover(\"" + mail_pd_id + "\")'>恢复</a> | ";
            content += "<a href='javascript:;' onclick='removeOrderReal(\"" + mail_pd_id + "\")'>彻底删除</a></td>";
        } else {
            content += "<td><a href='/order_mgr/order_detail/" + mail_pd_id + "' target='_blank'>详情</a> | ";
            content += "<a href='javascript:;' onclick='removeOrder(\"" + mail_pd_id + "\")'>删除</a></td></tr>";
        }
    }
    content += '</table>';
    content += '<div class="page_flag"></div>';
    $(".body_right").empty().append(content);
    pageAction(".page_flag", pageCallBack, result.data.total, result.data.page);
}
