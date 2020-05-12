
function edit_detail() {
    var labelArray = [];
    var spanArray = [];
    var classArray = [];
    for (var i=0; i<11; i++){
        labelArray.push($(".order_detail label:eq(" + i + ")").text());
        spanArray.push($(".order_detail span:eq(" + i + ")").text());
        classArray.push($(".order_detail span:eq(" + i + "), .order_detail a").attr("class"));
    }

    $(".body_right").empty();
    var content = '<div class="order_detail">';
    for (var i=0; i<11; i++) {
        console.log(labelArray[i], spanArray[i], classArray[i]);
        if (classArray[i] == "img_name") {
            content += '<p><label>' + labelArray[i] + '</label><a><input type="file" name="upload_order_img" id="upload_order_img"></a><span>如果未选择，则是之前上传的图片</span></p>'
        } else {
            content += '<p><label>' + labelArray[i] + '</label><input type="text" name="'+ classArray[i] +'" value="'+ spanArray[i] +'"></p>';
        }
    }
    content += '</div>';
    content += '<p class="edit_detail"><button type="button" onclick="update_detail()">确定</button></p>';
    $(".body_right").append(content);
}

function update_detail() {
    var formData= new FormData();
    var formDataArr = $(".order_detail").serializeArray();
    $.each(formDataArr, function (i, item) {
        formData.append(item.name, item.value)
    });

    var fileObj = $("#upload_order_img");
    if (fileObj.val()) {
        formData.append('upload_order_img', fileObj[0].files[0]);
    } else {
        formData.append('upload_order_img', "");
    }

    console.log(formData);

    // $.ajax({
    //     method: 'post',
    //     url: "/order_mgr/upload_order",
    //     data: formData,
    //     contentType: false,
    //     processData: false,
    //     success: function (result) {
    //         if (result.code != 0) {
    //             alert(result.msg);
    //             return;
    //         } else {
    //             orderSubmitSuccess();
    //         }
    //     },
    //     error: function () {
    //         alert('系统错误，稍后再试');
    //     }
    // })
}