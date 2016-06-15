/**
 * Created by houjincheng on 16/4/23.
 */

var operation = {
    getQueryString: function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = window.location.search.substr(1).match(reg);
        if(r != null) return unescape(r[2]);
        return null;
    }
};
module.exports = operation;