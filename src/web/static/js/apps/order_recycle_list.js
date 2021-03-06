$(window).load(function () {
    showOrderRecycleList();

});

// 回收站订单
function showOrderRecycleList(page) {
    getRequest(order_list_url, {"page": page || 1, "page_size": pageInfo.pageSize, "recycle": 1}, showOrderRecycleListSuccess);
}

function showOrderRecycleListSuccess(result) {
    orderContent(result, true, showOrderRecycleList, "目前没有订单被删除！");
}

// 搜索
function searchOrder() {
    searchOrderCommon(1, 1, showOrderRecycleListSuccess);
}

// 恢复
function removeOrderRecover(mail_pd_id) {
    removeOrderCommon(mail_pd_id, 1, removeOrderRecoverSuccess);
}

function removeOrderRecoverSuccess() {
    alert("恢复成功！");
    window.location.href = "/order_mgr/order_recycle"
}

// 彻底删除
function removeOrderReal(mail_pd_id) {
    removeOrderCommon(mail_pd_id, 2, removeOrderRealSuccess);
}

function removeOrderRealSuccess() {
    alert("彻底删除成功！");
    window.location.href = "/order_mgr/order_recycle"
}
