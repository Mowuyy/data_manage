function ajaxRequest(method, url, data, succCallback, errCallback=undefined) {
    var options = {
        url: url,
        method: method,
        dataType: 'json',
        error: function (xhr, textStatus, errorThrown) {
            if(errCallback)
                errCallback(xhr, textStatus, errorThrown);
            else{
                alert("系统错误,稍后再试");
            }
        },
        success: function (result) {
            if(result.code != 0){
                alert(result.msg);
                return;
            }
            succCallback(result);
        },
    };
    if(method != 'get'){
        options['contentType'] = 'application/json';
        if(data != null && data != undefined && typeof(data) != 'string'){
            data = JSON.stringify(data);
        }
    }
    options.data = data;
    $.ajax(options);
}

function getRequest(url, data, succCallback, loading=false, errCallback=undefined) {
    return ajaxRequest('get', url, data, succCallback, loading, errCallback);
}

function postRequest(url, data, succCallback, loading=false, errCallback=undefined) {
    return ajaxRequest('post', url, data, succCallback, loading, errCallback=undefined);
}