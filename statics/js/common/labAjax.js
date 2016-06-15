/**
 *  调用Ajax 入口页面
 */

module.exports = {
    requestOptions: {
        /**
         *  执行请求的方式默认为POST
         */
        type: "POST",
        /**
         *  是否为异步 默认为异步
         */
        async: true,
        /**
         *  是否缓存 默认为true
         */
        cache: true,
        /**
         *  请求数据
         */
        data: "",
        /**
         *  请求的网址
         */
        url: "",
        /**
         *  (默认: "application/json") 发送信息至服务器时内容编码类型
         */
        contentType: "application/json",
        /**
         *  异步加载时是否显示等待框
         */
        isShowWaitBar: false
    },
    getCookie: function (c_name) {
        if(document.cookie.length > 0){
            c_start = document.cookie.indexOf(c_name + "=")
            if(c_start != -1){
                c_start = c_start + c_name.length + 1
                c_end = document.cookie.indexOf(";", c_start)
                if(c_end == -1) c_end = document.cookie.length
                return unescape(document.cookie.substring(c_start, c_end))
            }
        }
        return ""
    },
    csrfSafeMethod: function (method) {
        // these http methods do not require csrf protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    },
    /**
     *  用参数对象执行异步请求
     *  @param param 请求数据对象
     *  @param url 请求URL
     *  @param successCall 成功执行的回调函数
     *  @param failCall 失败执行的回调函数
     */
    doRequestByParam: function (param, url, successCall, failCall, completeCall, isShowWaitBar) {
        this.doRequest({
            url: url,
            data: param,
            successCall: successCall,
            failCall: failCall,
            completeCall: completeCall,
            isShowWaitBar: false
        });
    },
    /**
     * 用json串请求
     * @param url 请求URL
     * @param jsonParamStr 向服务器发送的json串
     * @param successCall 成功执行的回调函数
     * @param failCall 失败执行的回调函数
     * @param completeCall
     * @param isShowWaitBar
     */
    doRequestByJsonStr: function(url, jsonParamStr, successCall, failCall, completeCall, isShowWaitBar){
        this.doRequest({
            url: url,
            data: JSON.stringify(jsonParamStr),
            contentType: "application/json",
            successCall: successCall,
            failCall: failCall,
            isShowWaitBar: isShowWaitBar
        });
    },
    doRequest: function (option){
        //异步调用
        if(option.isShowWaitBar){
            //todo 显示数据加载等待框
        }
        var options = $.extend({}, this.requestOptions, option);
        var that = this;
        var csrftoken = that.getCookie("csrftoken");

        this.requestOptions.xhr = $.ajax({
            type: options.type, //get post
            async: options.async, //false true
            cache: options.cache,
            url: options.url,
            data: options.data,
            contentType: options.contentType,
            beforeSend: function (xhr, settings){
                if (!that.csrfSafeMehtod(settings.type) && !this.crossDomain){
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            /**
             *  请求成功后处理的方法
             *  @param result 返回的结果
             */
            success: function(result){
                if(options.successCall){
                    options.successCall.call(this, result);
                }
            },
            /**
             * 请求完成后的处理方法
             * @param xmlhttprequest xmlhttprequest 对象
             * @param testStatus 描述成功请求类型的字符串
             */
            complete: function(XMLHttpRequest, textStatus){
                if(options.sucessCall){
                    options.sucessCall.call(this, XMLHttpRequest, textStatus);
                }
                if(XMLHttpRequest.getResponseHeader('skipURL')){
                    window.location.href = XMLHttpRequest.getResponseHeader('skipURL');
                }
            },
            /**
             * 请求失败后的处理方法
             * @param jqXHR 被jquery 包装过的XMLHttpRequest 对象
             * @param textStatus 错误状态, 可能的值有 "timeout", "error", "abort", "parsererror"
             * @param errorThrown 出现http 错误时(即testStatus 为 error时)的http 错误信息, 例如"Not Found", "Internal Server Error"
             */
            error: function(jqXHR, textStatus, errorThrown){
                if(options.failCall) {
                    options.failCall.call(this, jqXHR, textStatus, errorThrown)
                }else{
                    if(textStatus != "abort" && jqXHR.status != 0){

                    }
                }
            }
        })
    }
}