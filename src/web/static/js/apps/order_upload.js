// 订单上传
function orderSubmit() {
    var formData= new FormData();
    var formDataArr = $("#upload_order_form").serializeArray();
    $.each(formDataArr, function (i, item) {
        formData.append(item.name, item.value)
    });
    var fileObj = $("#upload_order_img");
    if (fileObj.val()) {
        formData.append('upload_order_img', fileObj[0].files[0]);
    } else {
        formData.append('upload_order_img', "");
    }
    formRequest("/order_mgr/upload_order", formData, orderSubmitSuccess);
}

function orderSubmitSuccess() {
    alert("订单上传成功！");
    window.location.href = "/order_mgr/render_upload"
}

