$(window).load(function () {
    showOrderList();
});

// 列表页
function showOrderList(page) {
    getRequest(order_list_url, {"page": page || 1, "page_size": pageInfo.pageSize}, showOrderListSuccess);
}

function showOrderListSuccess(result) {
    orderContent(result, false, showOrderList, "目前没有上传订单数据！")
}

// 搜索
function searchOrder() {
    searchOrderCommon(1, 0, showOrderListSuccess);
}

// 删除
function removeOrder(orderId) {
    removeOrderCommon(orderId, 0, removeOrderSuccess);
}

function removeOrderSuccess() {
    alert("订单删除成功！");
    showOrderList();
}

