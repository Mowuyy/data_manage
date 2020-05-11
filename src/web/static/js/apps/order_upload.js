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
