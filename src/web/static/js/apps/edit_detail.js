var orderStatus = {
    1: "退货",
    2: "退改",
    3: "丢件",
    4: "其他"
};

function editDetail() {
    var labelArray = [];
    var spanArray = [];
    var classArray = [];
    for (var i=0; i<11; i++){
        labelArray.push($(".order_detail label:eq(" + i + ")").text());
        spanArray.push($(".order_detail span:eq(" + i + ")").text());
        classArray.push($(".order_detail span:eq(" + i + "), .order_detail a").attr("class"));
    }

    $(".body_right").empty();
    var content = '<form class="order_detail">';
    for (var i=0; i<11; i++) {
        if (classArray[i] == "img_name") {
            content += '<p><label>' + labelArray[i] + '</label><a><input type="file" name="upload_order_img" id="upload_order_img"></a><span>如果未选择，则是之前上传的图片</span></p>'
        } else if (classArray[i] == "order_status"){
            content += '<p><label>订单状态: </label><select class="order_status" name="order_status">';
            for (var j=1; j<5; j++) {
                if (orderStatus[j] == spanArray[i] ) {
                    content += '<option value="'+ j +'" selected="selected">' + orderStatus[j] + '</option>';
                } else {
                    content += '<option value="'+ j +'">' + orderStatus[j] + '</option>';
                }
            }
            content += '</select></p>';
        } else if (classArray[i] == "mail_pd_id") {
            content += '<p><label>' + labelArray[i] + '</label><span id="mail_pd_id">'+ spanArray[i] +'</span></p>';
        } else {
            content += '<p><label>' + labelArray[i] + '</label><input type="text" name="'+ classArray[i] +'" value="'+ spanArray[i] +'"></p>';
        }
    }
    content += '<p class="edit_detail"><button type="button" onclick="updateDetail()">确定</button></p>';
    content += '</form>';
    $(".body_right").append(content);
}

var mail_pd_id = null;
function updateDetail() {
    var formData= new FormData();
    var formDataArr = $(".order_detail").serializeArray();
    $.each(formDataArr, function (i, item) {
        formData.append(item.name, item.value);
    });
    var fileObj = $("#upload_order_img");
    if (fileObj.val()) {
        formData.append('upload_order_img', fileObj[0].files[0]);
    } else {
        formData.append('upload_order_img', "");
    }
    mail_pd_id = $("#mail_pd_id").text();
    formData.append("mail_pd_id", mail_pd_id);
    formData.append("action", "edit");
    formRequest("/order_mgr/upload_order", formData, updateDetailSuccess);
}

function updateDetailSuccess() {
    alert("修改成功！");
    window.location.href = '/order_mgr/order_detail/' + mail_pd_id;
}