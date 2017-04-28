/**
 * Created by waltergomez on 4/5/17.
 */

(function( $ ){
    $.myPOST = function( url, data, success ) {
        var settings = {
            type : "POST", //predefine request type to POST
            'url'  : url,
            'data' : data,
            'timeout' : 100000000,
            'success' : success,
            'error': function(){
                    alert("error4")
            }
        };
        $.ajax(settings)
    };
})( jQuery );

function usChangeEventHadler(numFreqUS){
    //alert("chang on " + numFreqUS);
    var i=numFreqUS+1;
}



function usModChangeEventHadler(numFreqUS){

    i=numFreqUS+1;
    var freqUsUL= "freqUsUL"+i;
    var numUSperSG = document.getElementById('uspersg').value;
    var actualNumUsFreq=document.getElementById('listUSfreq').childElementCount;

    //alert("change on Mod " + numFreqUS + "  actual  " + actualNumUsFreq);

    if((numFreqUS==actualNumUsFreq)&&(actualNumUsFreq+1<numUSperSG)) {
        newLine = '<li class="list-group-item " id="USfreq' + i + '">Freq' + i + '<input type="number" id="' + freqUsUL
            + '" placeholder="freq' + i + '" onchange="usChangeEventHadler(' + i + ')" > Mhz  Modulation' +
            '<select id="usmod' + i + '" name="usmod' + i + '" onchange="usModChangeEventHadler(' + i + ')"> ' +
            '<option value="0">--</option> ' +
            '<option value="TDMA">TDMA</option>' +
            '<option value="ATDMA">ATDMA</option>' +
            '</select>' +
            '<select id="uscod'+i+'" name="uscod' + i + '"> ' +
            '<option value="--">--</option> ' +
            '<option value="QPSK">QPSK</option> ' +
            '<option value="QAM16">QAM16</option> ' +
            '<option value="QAM64">QAM64</option> ' +
            '</select>' + 'Channel Width ' +
            '<select id="uswidth'+i+'" > ' +
            '<option value="--">--</option> ' +
            '<option value="3.2">3.2</option> ' +
            '<option value="6.4">6.4</option> ' +
            '</select>'+
            '</li>';

        $('#listUSfreq').append(newLine);
    }

}


function reviewUSFreq(numUSperSG){
    var initialFreq=Number(document.getElementById('usfreq0').value);
    var freqULus = "";
    var revfreqULus = "";
    var ulFrecuencyUS;
    var valFrecuencyus;
    var dif=0;
    var modulation=(document.getElementById('usmod1').value);

    //alert("function reviewUSFreq " + numUSperSG);
    $('#reviewUSfreq').empty();

    i=0;
    freqULus = "freqUsUL"+i;
    revfreqUL = "revfreqUsUL"+i;
    //ulFrecuency = document.getElementById(freqUL);
    valFrecuency = initialFreq;

    newLine = '<li class="list-group-item " id="revUSfreq' + i + '">Freq' + i + '<input type="text" id="' + revfreqUL +
        '" placeholder="' + valFrecuency +'" disabled  > Mhz   Modulation ' + modulation + '</li><br>';

    $('#reviewUSfreq').append(newLine);


     for(var i = 1;i < numUSperSG;i++){
         freqULus = "freqUsUL"+i;
         revfreqUL = "revfreqUsUL"+i

         ulFrecuency = document.getElementById(freqULus);
         valFrecuency = Number(ulFrecuency.value);

         newLine = '<li class="list-group-item " id="revUSfreq' + i + '">Freq' + i + '<input type="text" id="' + revfreqUL +
             '" placeholder="' + valFrecuency +'"disabled  > Mhz   Modulation ' + modulation + '</li><br>';

         $('#reviewUSfreq').append(newLine);

     }
}


function dsChangeEventHadler(numFreq){

    var freqUL = "freqUL"+numFreq;
    var ulFrecuency = document.getElementById(freqUL);
    var valFrecuencyChanged = Number(ulFrecuency.value);
    var dif=0;
    var ilChanged = "DSfreq"+numFreq;
    var objChange = document.getElementById(ilChanged);
    var numDSperSG = document.getElementById('dspersg').value;
    var freqIndex=numFreq+1;


    //alert("changed "+numFreq);
    if(numFreq==1){
        var initialFreq=Number(document.getElementById('freq0').value);
        dif=valFrecuencyChanged-initialFreq;
        if(dif<6){
            //alert("Frec Overlap " + dif);
            ulFrecuency.setAttribute("class", "list-group-item-danger");
            objChange.setAttribute("class", "list-group-item-danger");

        }
        else{
            ulFrecuency.setAttribute("class", "list-group-item-success");
            objChange.setAttribute("class", "list-group-item-success");
        }
    }
    else{
        var prevElement="freqUL"+(numFreq-1)
        //alert(prevElement);
        var prevFreq=Number(document.getElementById(prevElement).value);
        dif=valFrecuencyChanged-prevFreq;
        if(dif<6){
            alert("Frec Overlap " + dif);
            ulFrecuency.setAttribute("class", "list-group-item-danger");
            objChange.setAttribute("class", "list-group-item-danger");

        }
        else{
            ulFrecuency.setAttribute("class", "list-group-item-success");
            objChange.setAttribute("class", "list-group-item-success");
        }
    }

}

function reviewDSFreq(numDSperSG){
    var initialFreq=Number(document.getElementById('freq0').value);
    var freqUL = "";
    var revfreqUL = "";
    var ulFrecuency;
    var valFrecuency;
    var dif=0;

    //alert("function reviewDSFreq");

     $('#reviewDSfreq').empty();

     i=0;
     freqUL = "freqUL"+i;
     revfreqUL = "revfreqUL"+i;
     //ulFrecuency = document.getElementById(freqUL);
     valFrecuency = initialFreq;
     newLine='<li class="list-group-item " id="revDSfreq'+i+'">Freq'+i+'<input type="number" id="'+ revfreqUL
     +'" placeholder="'+valFrecuency+'" disabled > Mhz</li><br>';

     $('#reviewDSfreq').append(newLine);
     var valFreqAnterior=initialFreq;
     var ulFrecuency = document.getElementById(revfreqUL);
     var ilChanged = "revDSfreq"+i;
     var objChange = document.getElementById(ilChanged);
     if(initialFreq>10){
     ulFrecuency.setAttribute("class", "list-group-item-success");
     objChange.setAttribute("class", "list-group-item-success");
     }
     else{
     ulFrecuency.setAttribute("class", "list-group-item-danger");
     objChange.setAttribute("class", "list-group-item-danger");

     }

     for(var i = 1;i < numDSperSG;i++){
     freqUL = "freqUL"+i;
     revfreqUL = "revfreqUL"+i;
     ulFrecuency = document.getElementById(freqUL);
     valFrecuency = Number(ulFrecuency.value);

     newLine='<li class="list-group-item " id="revDSfreq'+i+'">Freq'+i+'<input type="number" id="'+revfreqUL
     +'" placeholder="'+valFrecuency+'" disabled > Mhz</li><br>';

     $('#reviewDSfreq').append(newLine);

     dif=valFrecuency-valFreqAnterior;

     if(dif<6){
     ilChanged = "revDSfreq"+i;
     ulFrecuency = document.getElementById(revfreqUL)
     objChange = document.getElementById(ilChanged);

     ulFrecuency.setAttribute("class", "list-group-item-danger");
     objChange.setAttribute("class", "list-group-item-danger");


     }
     else{
     ilChanged = "revDSfreq"+i;
     ulFrecuency = document.getElementById(revfreqUL)
     objChange = document.getElementById(ilChanged);

     ulFrecuency.setAttribute("class", "list-group-item-success");
     objChange.setAttribute("class", "list-group-item-success");
     }

     valFreqAnterior=valFrecuency;

     }

}


function generateDSfs(){

    var dsContiguousFreq = document.getElementById('dsContigFreq').checked;
    var numDSperSG = document.getElementById('dspersg').value;
    var initialFreq=Number(document.getElementById('freq0').value);
    var idFreq="";
    var freqUL="";
    var strFreqUL="";
    var elemento;
    var listOfFrequencies=document.getElementById('listDSfreq');
    var newLine="";
    var editable="";
    var ilChanged = "";
    var objChange;

    //alert("initial freq" + initialFreq + "  numDSperSG  " + numDSperSG);
    //return false;

    if(dsContiguousFreq==true){
        editable="disabled";
    }

    $('#listDSfreq').empty();


    for(var i = 1;i < numDSperSG;i++){
        ilChanged = "DSfreq"+i;

        freqUL = "freqUL"+i;
        strFreqUL="'#"+freqUL+"'";

        newLine='<li class="list-group-item " id="DSfreq'+i+'">Freq'+i+'<input type="number" id="'+ freqUL
            + '" placeholder="freq'+i+'" '+editable+'onchange="dsChangeEventHadler('+i+')" > Mhz</li><br>';


        $('#listDSfreq').append(newLine);

        if(dsContiguousFreq==true){
            idFreq = "DSfreq"+i;

            //alert(freqUL);
            elemento=document.getElementById(freqUL);
            elemento.placeholder=initialFreq+6*i;
            elemento.value=initialFreq+6*i;
            elemento.setAttribute("class", "list-group-item-success");
            objChange = document.getElementById(ilChanged);
            objChange.setAttribute("class", "list-group-item-success");


        }
        else{
            elemento=document.getElementById(freqUL);
            elemento.placeholder="freq"+i;
            elemento.value="freq"+i;
        }

    }


}

function callWSsetControllerIntegratedCable(){
    var objChange = document.getElementById('processIntCableCtrlBtn');
    var urlWSsetControllerIntegratedCable = '/setControllerIntegratedCable/';
    var numDSperSG = document.getElementById('dspersg').value;
    var initialFreq=Number(document.getElementById('freq0').value);
    var device= document.getElementById('valueCMTS').value;
    var endDS = numDSperSG - 1;
    var sgarch = document.getElementById('sgarch').value;
    var dataType='application/vnd.yang.data+json';
    var sgs=document.getElementById('sgs').value;
    initialFreq=initialFreq*1000000;
    //alert("numDS= " + numDSperSG + " endDS= " + endDS + " device= " + device + " sgarch= " + sgarch)

    urlWSsetControllerIntegratedCable=urlWSsetControllerIntegratedCable+sgs+"/"+sgarch
    //alert(urlWSsetControllerIntegratedCable)

    //document.getElementById("processIntCableCtrlBtn").disabled = true;

    dataPost='{"device": "'+device + '", ' +
        '"numDS": "' + numDSperSG+'", ' +
        '"freqIni": "' + initialFreq+'", ' +
        '"endDS": "' + endDS+'"' +
        '}';

    //alert(dataPost);

    //$(selector).post(URL,data,function(data,status,xhr),dataType)

    $.myPOST(urlWSsetControllerIntegratedCable,dataPost, function(data,status){

        //alert(result);
        document.getElementById("processIntCableCtrlBtn").disabled = false;

        alert("Status Code==" + status)
        if(status=="success"){
            objChange.setAttribute("class", "list-group-item-success");
        }
        else{
            objChange.setAttribute("class", "list-group-item-warning");
        }

    });

}


function callWSsetControllerUpstreamCable(){
    var objChange = document.getElementById('processUSCableCtrlBtn');
    var urlWSsetControllerUpstreamCable = '/setControllerUpstreamCable/';
    var numUSperSG = Number(document.getElementById('uspersg').value);
    var device= document.getElementById('valueCMTS').value;
    var sgarch = Number(document.getElementById('sgarch').value);
    var dataType='application/vnd.yang.data+json';

    var usFreq0=Number(document.getElementById('usfreq0').value);
    var usMod0=document.getElementById('usmod0').value;
    var usCod0=document.getElementById('uscod0').value;
    var usWidth0=document.getElementById('uswidth0').value;
    var sgs=document.getElementById('sgs').value;

    usFreq0=usFreq0*1000000;
    usWidth0=usWidth0*1000000;
    //alert("uscod0= "+usCod0);
    if(usMod0=="TDMA"){
        usMod0="tdma";
        if(usCod0=="QPSK"){
            var usProfile0="21";
        }
        else{
            var usProfile0="22";
        }

    }
    if(usMod0=="ATDMA"){
        usMod0="atdma";
        if(usCod0=="QPSK"){
            var usProfile0="222";
        }
        if(usCod0=="QAM16"){
            var usProfile0="223";
        }
        else{
            var usProfile0="221";
        }

    }

    if(numUSperSG>1) {
        var usFreq1 = Number(document.getElementById('freqUsUL1').value);
        var usMod1 = document.getElementById('usmod1').value;
        var usCod1 = document.getElementById('uscod1').value;
        var usWidth1 = document.getElementById('uswidth1').value;
        usWidth1=usWidth1*1000000;
        usFreq1=usFreq1*1000000;
        if(usMod1=="TDMA"){
            usMod1="tdma";
            if(usCod1=="QPSK"){
                var usProfile1="21";
            }
            else{
                var usProfile1="22";
            }
        }
        if(usMod1=="ATDMA"){
            usMod1="atdma";
            if(usCod1=="QPSK"){
                var usProfile1="222";
            }
            if(usCod1=="QAM16"){
                var usProfile1="223";
            }
            else{
                var usProfile1="221";
            }
        }
    }
    //alert("usMod1= "+ usMod1);
    if(numUSperSG>2) {
        var usFreq2 = Number(document.getElementById('freqUsUL2').value);
        var usMod2 = document.getElementById('usmod2').value;
        var usCod2 = document.getElementById('uscod2').value;
        var usWidth2 = document.getElementById('uswidth2').value;
        usWidth2=usWidth2*1000000;
        usFreq2=usFreq2*1000000;
        if(usMod2=="TDMA"){
            usMod2="tdma";
            if(usCod2=="QPSK"){
                var usProfile2="21";
            }
            else{
                var usProfile2="22";
            }
        }
        if(usMod2=="ATDMA"){
            usMod2="atdma";
            if(usCod2=="QPSK"){
                var usProfile2="222";
            }
            if(usCod2=="QAM16"){
                var usProfile2="223";
            }
            else{
                var usProfile2="221";
            }
        }
    }
    if(numUSperSG>3) {
        var usFreq3 = Number(document.getElementById('freqUsUL3').value);
        var usMod3 = document.getElementById('usmod3').value;
        var usCod3 = document.getElementById('uscod3').value;
        var usWidth3 = document.getElementById('uswidth3').value;
        usWidth3=usWidth3*1000000;
        usFreq3=usFreq3*1000000;
        if(usMod3=="TDMA"){
            usMod3="tdma";
            if(usCod3=="QPSK"){
                var usProfile3="21";
            }
            else{
                var usProfile3="22";
            }
        }
        if(usMod3=="ATDMA"){
            usMod3="atdma";
            if(usCod3=="QPSK"){
                var usProfile3="222";
            }
            if(usCod3=="QAM16"){
                var usProfile3="223";
            }
            else{
                var usProfile3="221";
            }
        }
    }

    var dataPost='{"device": "'+device + '", ' +
        '"freq0": "' + usFreq0+'", ' +
        '"width0": "' + usWidth0+'", ' +
        '"mode0": "' + usMod0+'", ' +
        '"prof0": "' + usProfile0+'"';

    if(numUSperSG>1) {
        dataPost= dataPost + "," + '"freq1": "' + usFreq1+'", ' +
            '"width1": "' + usWidth1+'", ' +
            '"mode1": "' + usMod1+'", ' +
            '"prof1": "' + usProfile1+'"';
    }
    if(numUSperSG>2) {
        dataPost= dataPost + ","+ '"freq2": "' + usFreq2+'", ' +
            '"width2": "' + usWidth2+'", ' +
            '"mode2": "' + usMod2+'", ' +
            '"prof2": "' + usProfile2+'"';
    }
    if(numUSperSG>3) {
        dataPost= dataPost+ "," + '"freq3": "' + usFreq3+'", ' +
            '"width3": "' + usWidth3+'", ' +
            '"mode3": "' + usMod3+'", ' +
            '"prof3": "' + usProfile3+'"';
    }

    dataPost = dataPost + '}';
    //alert (dataPost)


    urlWSsetControllerUpstreamCable=urlWSsetControllerUpstreamCable+sgs+"/"+sgarch
    //alert(urlWSsetControllerUpstreamCable)


    //document.getElementById("processUSCableCtrlBtn").disabled = true;

    //$(selector).post(URL,data,function(data,status,xhr),dataType)
    $.myPOST(urlWSsetControllerUpstreamCable,dataPost, function(data,status){

        //alert(result);
        document.getElementById("processUSCableCtrlBtn").disabled = false;

        alert("Status Code==" + status)
        if(status=="success"){
            objChange.setAttribute("class", "list-group-item-success");
        }
        else{
            objChange.setAttribute("class", "list-group-item-warning");
        }

    });


}

function callWSsetInterfaceCable(){
    var objChange = document.getElementById('processIntCableBtn');
    var urlWSsetInterfaceCable = '/setInterfaceCable/';
    var numDSperSG = document.getElementById('dspersg').value;
    var device= document.getElementById('valueCMTS').value;
    var endDS = numDSperSG - 1;
    var sgarch = document.getElementById('sgarch').value;
    var dataType='application/vnd.yang.data+json';
    var idbundle=document.getElementById('idbundle1').value;
    var sgs=document.getElementById('sgs').value;
    var numUSperSG = Number(document.getElementById('uspersg').value);

    //alert("numUSperSG= " + numUSperSG + " endDS= " + endDS + " device= " + device + " sgarch= " + sgarch + " idbundle=" + idbundle + "  sgs" + sgs)


    urlWSsetInterfaceCable=urlWSsetInterfaceCable+sgs+"/"+sgarch+"/"+numUSperSG
    //alert(urlWSsetInterfaceCable)



    var dataPost='{"device": "'+device + '", ' +
        '"ipBundle": "' + idbundle+'", ' +
        '"numDS": "' + endDS+'"' +
        '}';

    //alert(dataPost);

    //document.getElementById("processIntCableBtn").disabled = true;

    //$(selector).post(URL,data,function(data,status,xhr),dataType)
    $.myPOST(urlWSsetInterfaceCable,dataPost, function(data,status){

        //alert(result);
        document.getElementById("processIntCableCtrlBtn").disabled = false;

        alert("Status Code==" + status)
        if(status=="success"){
            objChange.setAttribute("class", "list-group-item-success");
        }
        else{
            objChange.setAttribute("class", "list-group-item-warning");
        }

    });

}


function callWSsetIntIntegratedCable(){
    var objChange = document.getElementById('processIntegratedCableBtn');
    var urlWSsetIntIntegratedCable = '/setIntIntegratedCable/';
    var numDSperSG = document.getElementById('dspersg').value;
    var device= document.getElementById('valueCMTS').value;
    var endDS = numDSperSG - 1;
    var sgarch = document.getElementById('sgarch').value;
    var dataType='application/vnd.yang.data+json';
    var idbundle=document.getElementById('idbundle1').value;
    var sgs=document.getElementById('sgs').value;
    var numUSperSG = Number(document.getElementById('uspersg').value);

    //alert("numUSperSG= " + numUSperSG + " endDS= " + endDS + " device= " + device + " sgarch= " + sgarch + " idbundle=" + idbundle + "  sgs" + sgs)


    urlWSsetIntIntegratedCable=urlWSsetIntIntegratedCable+sgs+"/"+sgarch+"/"+numDSperSG
    //alert(urlWSsetIntIntegratedCable)



    var dataPost='{"device": "'+device + '", ' +
        '"idBundle": "' + idbundle+'"' +
        '}';

    //alert(dataPost);


    //document.getElementById("processIntegratedCableBtn").disabled = true;

    //$(selector).post(URL,data,function(data,status,xhr),dataType)
    $.myPOST(urlWSsetIntIntegratedCable,dataPost, function(data,status){

        //alert(result);
        document.getElementById("processIntegratedCableBtn").disabled = false;

        alert("Status Code==" + status)
        if(status=="success"){
            objChange.setAttribute("class", "list-group-item-success");
        }
        else{
            objChange.setAttribute("class", "list-group-item-warning");
        }

    });

}


function callWSsetIntWideBand(){
    var objChange = document.getElementById('processIntWideBandBtn');
    var urlWSsetIntWideBand = '/setIntWideBand/';
    var numDSperSG = document.getElementById('dspersg').value;
    var device= document.getElementById('valueCMTS').value;
    var endDS = numDSperSG - 1;
    var sgarch = document.getElementById('sgarch').value;
    var dataType='application/vnd.yang.data+json';
    var idbundle=document.getElementById('idbundle1').value;
    var sgs=document.getElementById('sgs').value;
    var numUSperSG = Number(document.getElementById('uspersg').value);

    //alert("numUSperSG= " + numUSperSG + " endDS= " + endDS + " device= " + device + " sgarch= " + sgarch + " idbundle=" + idbundle + "  sgs" + sgs)


    urlWSsetIntWideBand=urlWSsetIntWideBand+sgs+"/"+sgarch+"/"+numDSperSG
    //alert(urlWSsetIntWideBand)



    var dataPost='{"device": "'+device + '", ' +
        '"idBundle": "' + idbundle+'"' +
        '}';

    //alert(dataPost);


    //document.getElementById("processIntWideBandBtn").disabled = true;

    //$(selector).post(URL,data,function(data,status,xhr),dataType)

    //$.post(urlWSsetIntWideBand,dataPost, function(data,status){

    $.myPOST(urlWSsetIntWideBand, dataPost, function(data,status){
        //alert("finish");

        document.getElementById("processIntWideBandBtn").disabled = false;

        alert("Status Code==" + status);
        if(status=="success"){
            objChange.setAttribute("class", "list-group-item-success");
        }
        else{
            objChange.setAttribute("class", "list-group-item-warning");
        }

    });

    /*$.ajax({
        type: "POST",
        url: urlWSsetIntWideBand,
        data: dataPost,
        async: true,
        success: function(data,status){
            //alert("finish");

            document.getElementById("processIntWideBandBtn").disabled = false;

            alert("Status Code==" + status);
            if(status=="success"){
                objChange.setAttribute("class", "list-group-item-success");
            }
            else{
                objChange.setAttribute("class", "list-group-item-warning");
            }

        },
        timeout: 100000,
        error: function(){
            alert("error3")
        }

    });
    */

}


function callWSsetCableFiberNode(){
    var objChange = document.getElementById('processCableFiberNodeBtn');
    var urlWSsetCableFiberNode = '/setCableFiberNode/';
    var numDSperSG = document.getElementById('dspersg').value;
    var device= document.getElementById('valueCMTS').value;
    var endDS = numDSperSG - 1;
    var sgarch = document.getElementById('sgarch').value;
    var dataType='application/vnd.yang.data+json';
    var idbundle=document.getElementById('idbundle1').value;
    var sgs=document.getElementById('sgs').value;
    var numUSperSG = Number(document.getElementById('uspersg').value);

    //alert("numUSperSG= " + numUSperSG + " endDS= " + endDS + " device= " + device + " sgarch= " + sgarch + " idbundle=" + idbundle + "  sgs" + sgs)


    urlWSsetCableFiberNode=urlWSsetCableFiberNode+sgs+"/"+sgarch
    //alert(urlWSsetCableFiberNode)



    var dataPost='{"device": "'+device + '"'+
        '}';

    //alert(dataPost);


    //document.getElementById("processCableFiberNodeBtn").disabled = true;

    //$(selector).post(URL,data,function(data,status,xhr),dataType)
    $.myPOST(urlWSsetCableFiberNode,dataPost, function(data,status){

        //alert(result);
        document.getElementById("processCableFiberNodeBtn").disabled = false;

        alert("Status Code==" + status)
        if(status=="success"){
            objChange.setAttribute("class", "list-group-item-success");
        }
        else{
            objChange.setAttribute("class", "list-group-item-warning");
        }

    });

}
