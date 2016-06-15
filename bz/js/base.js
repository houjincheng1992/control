/**
 * Created by baishengmei on 2016/5/13.
 */
$(function(){

    //delete function
    var $modul_contain = $("#modul_contain");
    var $delete = $("#delete");
    $delete.bind("click", function () {
        $(".modul_contain tbody input:checked").parent().parent().remove();//??????
    });

    //add function
    var $add = $("#add");
    var $addTable = $("#addTable");
    var $addTableTr = $("#addTable").find("tr");
    var $addOK = $("#addOK");
    var $showTable = $("#showTable");
    var $addClose = $("#addClose");
    function addMessage(){
        var addString={};
        for(var i=0; i<$addTableTr.length; i++){
            addString[i] = $($addTableTr[i]).find("input").val();
            addString[10] = $($addTableTr[10]).find("option").val();
        }
        var strTip;
        strTip = "<tr><td class='table-time'><input type='checkbox'>"+addString[0]+
                 "</td><td class='table-time'>"+addString[1]+
                 "</td><td class='table-time'>"+addString[2]+
                 '</td><td class="table-time">'+addString[3]+
                 '</td><td class="table-time">'+addString[4]+
                 '</td><td class="table-time">'+addString[5]+
                 '</td><td class="table-time">'+addString[6]+
                 '</td><td class="table-time">'+addString[7]+
                 '</td><td class="table-time">'+addString[8]+
                 '</td><td class="table-time">'+addString[9]+
                 '</td><td class="table-time">'+addString[10]+
//               '</td><td class="table-time">'+addString[11]+
//               '</td><td class="table-time">'+addString[12]+
//               '</td><td class="table-time">'+addString[13]+
//               '</td><td class="table-time">'+addString[14]+
                 "</td></tr>"
        $(strTip).appendTo($showTable);
        for(var j=0; j<$addTableTr.length; j++){
        $($addTableTr[j]).find("input").val("");
        }
        $addClose.click();
    }
    $addOK.bind("click", function(){
    	var flag = validateForm();
    	if(flag){
    		addMessage();
    	}
        
    });
//   $addClose.bind("click", function(){
////  	    $('table td').();
//  	    document.getElementsByTagName("td").style.background="white";
//      
//  });

    //modulation page
    var $modul_btn = $("#modul_btn");
    var $ais_modulation = $("#ais_modulation");
    $modul_btn.bind("click", function(){
        $ais_modulation.attr("class", "show").siblings().attr("class", "hidden");
        $modul_btn.attr("class", "active").siblings().attr("class", "");
    });

    //demodulation page
    var $ais_demodulation = $("#ais_demodulation");
    var $demodul = $("#demodul"); //demodulation button in the topbar
    var $demodul_btn = $("#demodul_btn");
    $demodul.bind("click", function(){
        $ais_demodulation.attr("class", "show").siblings().attr("class","hidden");
        $demodul_btn.attr("class", "active").siblings().attr("class", "");
    });
    $demodul_btn.bind("click", function(){
        $ais_demodulation.attr("class", "show").siblings().attr("class", "hidden");
        $demodul_btn.attr("class", "active").siblings().attr("class", "");
    });
    
    //analysis page
    var $analy_btn = $("#analy_btn");
    var ais_analysis = $("#ais_analysis");
    $analy_btn.bind("click", function(){
        ais_analysis.attr("class", "show").siblings().attr("class", "hidden");
        $analy_btn.attr("class", "active").siblings().attr("class", "");
    });
    
     //验证 function,action_all
    var $action_all= $("#action_all");
    $action_all.bind('focus', function(){
    	addOK.disabled=false;
    	document.getElementById("action_all").style.background="white";
    })
    $action_all.bind("blur",function(){
	    var text=document.getElementById("action_all").value; 
	    var regExp = /True|False/;
	    if(!regExp.test(text)){
	        document.getElementById("action_all").style.background="orangered";
	        document.getElementById("action_allcheck").style.visibility="hidden";
	    }
	    else{
			document.getElementById("action_all").style.background="white";
			addOK.disabled=false;
			document.getElementById("action_allcheck").style.visibility="visible";
		}
    });
    
      //验证 function,filename
    var $filename = $("#filename");
    $filename.bind('focus', function(){
    	addOK.disabled=false;
    	document.getElementById("filename").style.background="white";
    })
    $filename.bind("blur",function(){
	    var text=document.getElementById("filename").value; 
	   
	    if(text.length>20){
	        document.getElementById("filename").style.background="orangered";
	        document.getElementById("filenamecheck").style.visibility="hidden";
	    }
	    else{
			document.getElementById("filename").style.background="white";
			addOK.disabled=false;
			document.getElementById("filenamecheck").style.visibility="visible";
		}
    });
    //验证 function,lat
    var $lat = $("#lat");
    $lat.bind('focus', function(){
    	addOK.disabled=false;
    	document.getElementById("lat").style.background="white";
    })
    $lat.bind("blur",function(){
	    var text=document.getElementById("lat").value; 
	    var regExp = /^-?([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*|0?\.0+|0)$/;
	    if((!regExp.test(text))||text>90||text<-90){
	        document.getElementById("lat").style.background="orangered";
//	        $("#latcheck").display="none";
	        document.getElementById("latcheck").style.visibility="hidden";
	    }
	    else{
			document.getElementById("lat").style.background="white";
			addOK.disabled=false;
			document.getElementById("latcheck").style.visibility="visible";

		}
    });
     //验证 function,lon
    var $lon = $("#lon");
    $lon.bind('focus', function(){
    	addOK.disabled=false;
    	document.getElementById("lon").style.background="white";
    })
    $lon.bind("blur",function(){
	    var text=document.getElementById("lon").value; 
//	    var regExp = /^-?\d+$/; 
	    var regExp = /^-?([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*|0?\.0+|0)$/;
	   
	    if((!regExp.test(text))||text>180||text<-180){
	        document.getElementById("lon").style.background="orangered";
	         document.getElementById("loncheck").style.visibility="hidden";
	    }
	    else{
			document.getElementById("lon").style.background="white";
			document.getElementById("loncheck").style.visibility="visible";
			addOK.disabled=false;
		}
    });
    
     //验证 function,height
    var $height = $("#height");
    $height.bind('focus', function(){
    	addOK.disabled=false;
    	document.getElementById("height").style.background="white";
    })
    $height.bind("blur",function(){
	    var text=document.getElementById("height").value; 
//	    var regExp = /^\d+$/; 
	    var regExp = /^([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*)$/;
	   
	    if(!regExp.test(text)){
	        document.getElementById("height").style.background="orangered";
	        document.getElementById("heightcheck").style.visibility="hidden";
	    }
	    else{
			document.getElementById("height").style.background="white";
			document.getElementById("heightcheck").style.visibility="visible";
			addOK.disabled=false;
		}
    });
    
     //验证 function,vesnum
    var $vesnum = $("#vesnum");
    $vesnum.bind('focus', function(){
    	addOK.disabled=false;
    	document.getElementById("vesnum").style.background="white";
    })
    $vesnum.bind("blur",function(){
	    var text=document.getElementById("vesnum").value; 
	    var regExp = /^([1-9]\d*)$/; 
	   
	    if(!regExp.test(text)){
	        document.getElementById("vesnum").style.background="orangered";
	        document.getElementById("vesnumcheck").style.visibility="hidden";
	    }
	    else{
			document.getElementById("vesnum").style.background="white";
			document.getElementById("vesnumcheck").style.visibility="visible";
			addOK.disabled=false;
		}
    });
    
     //验证 function,obtime
    var $obtime = $("#obtime");
    $obtime.bind('focus', function(){
    	addOK.disabled=false;
    	document.getElementById("obtime").style.background="white";
    })
    $obtime.bind("blur",function(){
	    var text=document.getElementById("obtime").value; 
	    var regExp = /^([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*)$/; 
	   
	    if(!regExp.test(text)){
	        document.getElementById("obtime").style.background="orangered";
	        document.getElementById("obtimecheck").style.visibility="hidden";
	    }
	    else{
			document.getElementById("obtime").style.background="white";
			document.getElementById("obtimecheck").style.visibility="visible";
			addOK.disabled=false;
		}
    });
    
     //验证 function,ant_pitch
    var $ant_pitch = $("#ant_pitch");
    $ant_pitch.bind('focus', function(){
    	addOK.disabled=false;
    	document.getElementById("ant_pitch").style.background="white";
    })
    $ant_pitch.bind("blur",function(){
	    var text=document.getElementById("ant_pitch").value; 
	    var regExp = /^-?([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*|0?\.0+|0)$/;
	   
	    if((!regExp.test(text))||text>180||text<-180){
	        document.getElementById("ant_pitch").style.background="orangered";
	        document.getElementById("ant_pitchcheck").style.visibility="hidden";
	    }
	    else{
			document.getElementById("ant_pitch").style.background="white";
			document.getElementById("ant_pitchcheck").style.visibility="visible";
			addOK.disabled=false;
		}
    });
    
     //验证 function,ant_azimuth
    var $ant_azimuth = $("#ant_azimuth");
    $ant_azimuth.bind('focus', function(){
    	addOK.disabled=false;
    	document.getElementById("ant_azimuth").style.background="white";
    })
    $ant_azimuth.bind("blur",function(){
	    var text=document.getElementById("ant_azimuth").value; 
	    var regExp = /^-?([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*|0?\.0+|0)$/;
	   
	    if((!regExp.test(text))||text>360||text<0){
	        document.getElementById("ant_azimuth").style.background="orangered";
//	       	$("#ant_azimuthcheck").removeClass("checkV").addClass("check");
			document.getElementById("ant_azimuthcheck").style.visibility="hidden";
	    }
	    else{
			document.getElementById("ant_azimuth").style.background="white";
//			$("#ant_azimuthcheck").removeClass("check").addClass("checkV");
			document.getElementById("ant_azimuthcheck").style.visibility="visible";
			addOK.disabled=false;
		}
    });
      ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //校验lat字段是否提交
    function validateFormlat(){
    	var flag = true;
    	var regExp = /^-?([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*|0?\.0+|0)$/;
    	var text=document.getElementById("lat").value; 
	    if((!regExp.test(text))||text>90||text<-90){
	        document.getElementById("lat").style.background="orangered";
	        flag = false;
	        addOK.disabled=true;
	    } 
	    else{
			document.getElementById("lat").style.background="white";	
			addOK.disabled=false;
		}
	    return flag;
    }
    //校验lon字段 是否提交
    function validateFormlon(){
    	var flag = true;
    	var regExp = /^-?([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*|0?\.0+|0)$/;
    	var text=document.getElementById("lon").value; 
	    if((!regExp.test(text))||text>180||text<-180){
	        document.getElementById("lon").style.background="orangered";
	        flag = false;
	        addOK.disabled=true;
	    } 
	    else{
			document.getElementById("lon").style.background="white";	
			addOK.disabled=false;
		}
	    return flag;
    }
    //校验action_all字段是否提交
    function validateFormaction_all(){
    	var flag = true;
    	var text=document.getElementById("action_all").value; 
	    var regExp = /True|False/;
	    if(!regExp.test(text)){
	        document.getElementById("action_all").style.background="orangered";
	        flag = false;
	        addOK.disabled=true;
	    }
	    else{
			document.getElementById("action_all").style.background="white";
			addOK.disabled=false;
		}
	    return flag;
    }
    //校验filename字段是否提交
    function validateFormfilename(){
    	var flag = true;
    	 var text=document.getElementById("filename").value; 
	   
	    if(text.length>20){
	        document.getElementById("filename").style.background="orangered";
	        flag = false;
	        addOK.disabled=true;
	    }
	    else{
			document.getElementById("filename").style.background="white";
			addOK.disabled=false;
		}
	    return flag;
    }
    //校验height字段是否提交
    function validateFormheight(){
    	var flag = true;
    	var text=document.getElementById("height").value; 
	    var regExp = /^([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*)$/;
	   
	    if(!regExp.test(text)){
	        document.getElementById("height").style.background="orangered";
	        flag = false;
	        addOK.disabled=true;
	    }
	    else{
			document.getElementById("height").style.background="white";
			addOK.disabled=false;
		}
	    return flag;
    }
    //校验vesnum字段是否提交
    function validateFormvesnum(){
    	var flag = true;
    	var text=document.getElementById("vesnum").value; 
	    var regExp = /^([1-9]\d*)$/; 
	   
	    if(!regExp.test(text)){
	        document.getElementById("vesnum").style.background="orangered";
	        flag = false;
	        addOK.disabled=true;
	    }
	    else{
			document.getElementById("vesnum").style.background="white";
			addOK.disabled=false;
		}
	    return flag;
    }
    //校验obtime字段是否提交
    function validateFormobtime(){
    	var flag = true;
    	var text=document.getElementById("obtime").value; 
	    var regExp = /^([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*)$/; 
	   
	    if(!regExp.test(text)){
	        document.getElementById("obtime").style.background="orangered";
	        flag = false;
	        addOK.disabled=true;
	    }
	    else{
			document.getElementById("obtime").style.background="white";
			addOK.disabled=false;
		}
	    return flag;
    }
    //校验ant_pitch字段是否提交
    function validateFormant_pitch(){
    	var flag = true;
    	var text=document.getElementById("ant_pitch").value; 
	    var regExp = /^-?([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*|0?\.0+|0)$/;
	   
	    if((!regExp.test(text))||text>180||text<-180){
	        document.getElementById("ant_pitch").style.background="orangered";
	        flag = false;
	        addOK.disabled=true;
	    }
	    else{
			document.getElementById("ant_pitch").style.background="white";
			addOK.disabled=false;
		}
	    return flag;
    }
    //校验ant_azimuth字段是否提交
    function validateFormant_azimuth(){
    	var flag = true;
    	 var text=document.getElementById("ant_azimuth").value; 
	    var regExp = /^-?([1-9]\d*|[1-9]\d*\.\d*[1-9]\d*|0\.\d*[1-9]\d*|0?\.0+|0)$/;
	   
	    if((!regExp.test(text))||text>360||text<0){
	        document.getElementById("ant_azimuth").style.background="orangered";
	        flag = false;
	        addOK.disabled=true;
	    }
	    else{
			document.getElementById("ant_azimuth").style.background="white";
			addOK.disabled=false;
		}
	    return flag;
    }
    //校验是否提交
    function validateForm(){
    	var flag = false;
//  	var flag1 = validateFormuser();
    	var flag2 = validateFormaction_all();
    	var flag3 = validateFormfilename();
    	var flag4 = validateFormlat();
    	var flag5 = validateFormlon();
    	var flag6 = validateFormheight();
    	var flag7 = validateFormvesnum();
    	var flag8 = validateFormobtime();
    	var flag9 = validateFormant_pitch();
    	var flag10 = validateFormant_azimuth();
    	if(flag2&flag3&flag4&flag5&flag4&flag7&flag8&flag9&flag10){
    		flag=true;
    		addOK.disabled=false;
    		document.getElementById("latcheck").style.visibility="hidden";
    		document.getElementById("loncheck").style.visibility="hidden";
    		document.getElementById("action_allcheck").style.visibility="hidden";
    		document.getElementById("filenamecheck").style.visibility="hidden";
    		document.getElementById("heightcheck").style.visibility="hidden";
    		document.getElementById("vesnumcheck").style.visibility="hidden";
    		document.getElementById("obtimecheck").style.visibility="hidden";
    		document.getElementById("ant_pitchcheck").style.visibility="hidden";
    		document.getElementById("ant_azimuthcheck").style.visibility="hidden";
// 			$("table span > span").removeClass("checkV").addClass('check');
    		
    	}
    	else{
    		addOK.disabled=true;
    	}
    	return flag;
    }
  
//  $addOK.bind("click",function(e){
//  	e.preventDefault();
//  	var text=document.getElementById("idinput"); 
//	    if(text.value>100||text.value<-100){
//	        document.getElementById("idinput").style.background="orangered";
//	        xid="1";
//	    } else{
//	    	xid="0";
//			document.getElementById("idinput").style.background="white";
//			
//		}
//	    if(xid=="1"){
//	    	
//	    	addOK.disabled=true;
//	    }
//	    else{
//	    	addOK.disabled=false;
//	    }
//  });
    

});

    