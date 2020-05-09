var pageInfo = {
    "pageSize": 10
};

function pageAction(cssClass, callBackFunc, total, page) {
    $(cssClass).sPage({
        page: page,
        total: total,
        pageSize: pageInfo.pageSize,
        showTotal: true,
        totalTxt: "共{total}条",
        noData: false,
        showSkip: true,
        showPN: true,
        prevPage: "上一页",
        nextPage: "下一页",
        fastForward: 5,
        backFun: callBackFunc
    });
}

function requestSuccess(result, succCallback) {
    if(result.code != 0){
        alert(result.msg);
        return;
    }
    succCallback(result);
}

function requestError(xhr, textStatus, errorThrown, errCallback) {
    if(errCallback)
        errCallback(xhr, textStatus, errorThrown);
    else{
        alert("系统错误,稍后再试");
    }
}

function ajaxRequest(method, url, data, succCallback, errCallback=undefined) {
    var options = {
        url: url,
        method: method,
        dataType: 'json',
        error: function (xhr, textStatus, errorThrown) {
            requestError(xhr, textStatus, errorThrown, errCallback)
        },
        success: function (result) {
            requestSuccess(result, succCallback)
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
    return ajaxRequest('get', url, data, succCallback, errCallback);
}

function postRequest(url, data, succCallback, loading=false, errCallback=undefined) {
    return ajaxRequest('post', url, data, succCallback, errCallback);
}
