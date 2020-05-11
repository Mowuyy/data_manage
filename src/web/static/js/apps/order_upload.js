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

    $.ajax({
        method: 'post',
        url: "/order_mgr/upload_order",
        data: formData,
        contentType: false,
        processData: false,
        success: function (result) {
            if (result.code != 0) {
                alert(result.msg);
                return;
            } else {
                orderSubmitSuccess();
            }
        },
        error: function () {
            alert('系统错误，稍后再试');
        }
    })
}

function orderSubmitSuccess() {
    alert("订单上传成功！");
    $("#upload_order_form input").val("");
}

