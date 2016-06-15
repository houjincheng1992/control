/**
 *  总入口
 */

var React = require('react');
var labAjax = require('./common/labAjax.js');


//  请求的URl
var login_user_info_url = "/user/info";
var logout_url = "/logout";
var logout_redirect = "/login";
var no_auth_redirect = "/login";

var index = {
    //页面状态编码
    currentPage: {
        code : '0',
        name : 'index'
    },
    currentUser: {

    },
    //页面状态序列
    //依次序为: 总览, 调制, 解调, 信号分析
    pageArray: [
        'index', 'modulate', 'demodulate', 'analysis'
    ],
    //当前一级目录状态编码
    currentCategory: {
        code: '0',
        name: '总览'
    },
    //种别列表
    categoryArray: {
        'overview': '总览',
        'modulate': '调制',
        'demodulate': '解调',
        'analysis': '分析'
    },
    init: function () {
        // localStorage.removeItem("statusMonitor");
        popUpMsg.initMsgBox();
        // 设置默认区域与页面的title
        document.title = "星仔AIS仿真平台";
        // 拖动条原型链
        scale = function (btn, bar, title, obj) {
            var $this = this;
            setTimeout(function () {
                $this.btn = document.getElementById(btn);
                $this.bar = document.getElementById(bar);
                $this.title = document.getElementById(title);
                $this.step = $this.bar.getElementsByTagName("DIV")[0];
                $this.init(obj);
            }, 0)

        };
        scale.prototype = {
            init: function (obj) {
                var f = this, g = document, b = window, m = Math;
                if (obj.fullWidth) {
                    f.btn.style.left = '-0.963333px';
                    f.step.style.width = '17.0367px';
                } else {
                    f.btn.style.left = '3px';
                    f.step.style.width = '19px';
                }
                f.btn.onmousedown = function (e) {
                    var x = (e || b.event).clientX;
                    var l = this.offsetLeft;
                    if (obj.thisX) {
                        thisX = obj.thisX;
                    }
                    var max = f.bar.offsetWidth - this.offsetWidth;
                    var tur = true;
                    g.onmousemove = function (e) {
                        var thisX = (e || b.event).clientX;
                        var to = m.min(max, m.max(-2, l + (thisX - x)));
                        f.btn.style.left = to + 'px';
                        f.ondrag(m.round(m.max(0, to / max) * 100), to, obj);
                        b.getSelection ? b.getSelection().removeAllRanges() : g.selection.empty();
                    };
                    var that = this;
                    g.onmouseup = function (e) {
                        this.onmousemove = null;
                        obj.setPrice(f.title.value, obj.state.count);
                        this.onmouseup = null;
                    }
                };
                this.title.focus();
                setTimeout(function () {
                    this.title.blur();
                }.bind(this))
            },
            ondrag: function (pos, x, obj) {
                var that = this;
                this.step.style.width = (+Math.max(0, x) + 16) + 'px';
                if (obj.fullWidth) {
                    this.title.value = obj.fullWidth * pos * 0.01;
                    obj.setState({bandwidth: that.title.value});
                } else {
                    this.title.value = 1000 * pos * 0.01;
                    obj.setState({size: that.title.value});
                }
            }
        }
        if (true) {
            //获取用户登陆信息
            labAjax.doRequest({
                type: 'get',
                async: true,
                cache: true,
                url: login_user_info_url,
                data: null,
                contentType: 'application/json',
                successCall: function (data){
                    if (data.user.username) {
                        index.currentUser = data;
                        this.initHeader();
                        this.initAside();
                        this.setCurrentPage();
                        this.bindRefreshContent();
                    }else {
                        location.href = '/login';
                    }
                }.bind(this)
            });
        } else {
            window.location = "/compatibility";
        }
    },
    checkNavigator: function () {
        var browser = navigator.appName;
        var b_version = navigator.appVersion;
        var version = b_version.split(";");
        //检测是否是IE
        if ("ActiveXObject" in window) {
            if (version.length > 1) {
                var trim_Version = parseInt(version[1].replace(/[ ]/g, "").replace(/MSIE/g, ""));
                if (trim_Version < 10){
                    return false;
                } else {
                    return true;
                }
            }else {
                return false;
            }
        } else {
            return true;
        }
    },
    
    setSingleBindFunction: function () {
        
    }
}