/**
 * Created by zyt on 2016/6/14.
 */
 //验证 function,type_name_de
 //   var $type_name_de = $("#type_name_de");
$(function() {
    var $addOKDemodul = $("#addOKDemodul");
    $("#addModalDemodul").on('focus', "#type_name_de", function () {
        $("#addOKDemodul").attr("disabled",false);
        document.getElementById("type_name_de").style.background = "white";
    })
    $("#addModalDemodul").on('blur', "#type_name_de", function () {
        var text1 = document.getElementById("type_name_de").value;

        if (text1.length > 20 || text1 == null || text1 == "") {
            document.getElementById("type_name_de").style.background = "orangered";
            document.getElementById("type_name_decheck").style.visibility = "hidden";
            $addOKDemodul.attr("disabled",true);
        }
        else {
            document.getElementById("type_name_de").style.background = "white";
            $("#addOKDemodul").attr("disabled",false);
            document.getElementById("type_name_decheck").style.visibility = "visible";
        }
    });

    $('#addModalDemodul').on('click','#addOKDemodul',function() {
        if (!($("#addOKDemodul").disable)) {
            var addStringDemodul = {};
            var $showTableDemodul = $("#showTableDemodul")
            var $addTableDemodulTr = $("#addTableDemodul").find("tr");
            for (var i = 1; i < $addTableDemodulTr.length; i++) {
                addStringDemodul[i] = $($addTableDemodulTr[i]).find("option").val();
            }
            addStringDemodul[0] = $($addTableDemodulTr[0]).find("input").val();
            var strTipDemodul;
            strTipDemodul = "<tr><td class='table-time'><input type='checkbox'>" + addStringDemodul[0] +
                "</td><td class='table-time'>" + addStringDemodul[1] +
                "</td><td class='table-time'>" + addStringDemodul[2] +
                "</td><td class='table-time'>" + addStringDemodul[3] +
                "</td><td class='table-time'>" + addStringDemodul[4] +
                "</td></tr>"
            $(strTipDemodul).appendTo($showTableDemodul);
            $("#addClose").click();
        }
    });

});
