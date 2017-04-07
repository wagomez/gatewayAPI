/**
 * Created by waltergomez on 3/30/17.
 */



function callWSloadBalance(targetcmts, cLbD2,cLbD3){
    var url = 'http://127.0.0.1:8000/setLoadBalance/'+targetcmts+'/'+cLbD2+'/'+cLbD3;
    //alert(url);
    var xhttp = new XMLHttpRequest();

    xhttp.open('GET', url, false);
    xhttp.send(null);
}


function callWSgetDevices(){
    var urlCMTS = 'http://127.0.0.1:8000/getDevicesCMTS';
    var urlPE = 'http://127.0.0.1:8000/getDevicesPE';
    //alert(url);
    //var xhttp = new XMLHttpRequest();

    //xhttp.open('GET', url, false);
    //xhttp.send(null);

    //var resp = xhttp.response;

    $.getJSON(urlCMTS, function(result){

        //alert(result.cmts);
        var listOfCmts = document.getElementById('listOfCmts');
        //listOfCmts.enable();
        $('#listOfCmts').enabled;
        $.each(result.cmts, function(i, field){
            //alert(field);
            var cmtsName = field;

            //<option value="MA">MA</option>

            var info = '';
            var info = info + '<option value="' + cmtsName + '">' + cmtsName + '</option>';
            //alert (info);

            $('#listOfCmts').append(info);


        });



    });


    $.getJSON(urlPE, function(result){

        //alert(result.cmts);
        $.each(result.pe, function(i, field){
            //alert(field);
            var peName = field;

            //<option value="MA">MA</option>

            var info = '';
            var info = info + '<option value="' + peName + '">' + peName + '</option>';
            //alert (info);

            $('#listOfPE').append(info);

        });



    });

    $('#listDevices').show();
    //alert(resp)
}


$(document).ready(function(){



    $('#reviewBtn').click(function(){
        //var cmts = document.getElementById('deviceCMTS').value;
        var pe = document.getElementById('listOfPE').value;
        var cmts = document.getElementById('listOfCmts').value;
        var loadbalanceD2 = document.getElementById('loadbalancingD2').checked;
        var loadbalanceD3 = document.getElementById('loadbalancingD3').checked;
        var cmtsRedundancy = document.getElementById('cmtsRedundancy').checked;
        var numDSperSG = document.getElementById('dspersg').value;
        var numUSperSG = document.getElementById('uspersg').value;

        if(cmts=="--"){
            var objecto = document.getElementById("valueCMTS");
            objecto.setAttribute("class", "list-group-item-danger");
        }
        else{
            var objecto = document.getElementById("valueCMTS");
            objecto.setAttribute("class", "list-group-item-success");
        }
        if(pe=="--"){
            var objecto2 = document.getElementById("valuePE");
            objecto2.setAttribute("class", "list-group-item-danger");
        }
        else{
            var objecto2 = document.getElementById("valuePE");
            objecto2.setAttribute("class", "list-group-item-success");
        }
        $('#valueCMTS').val(cmts);
        $('#valuePE').val(pe);
        $('#valueLoadBalanceD2').val(loadbalanceD2);
        $('#valueLoadBalanceD3').val(loadbalanceD3);
        $('#valueCmtsRedundancy').val(cmtsRedundancy);

        reviewDSFreq(numDSperSG);
        reviewUSFreq(numUSperSG);

        //alert(loadbalanceD2);
        $('#processAll').show()
        $('#valores').show();
        $('#DSValues').show();
        $('#USValues').show();




    });


    $('#lbBtn').click(function(){

        //alert("click");

        var targetcmts = document.getElementById('listOfCmts').value;
        var bloadbalanceD2 = document.getElementById('loadbalancingD2').checked;
        var bloadbalanceD3 = document.getElementById('loadbalancingD3').checked;
        var cLbD3="";
        var cLbD2="";
        //alert(targetcmts);

        if (bloadbalanceD2==true)
            cLbD2="1"
        else
            cLbD2="0"
        if (bloadbalanceD3==true)
            cLbD3="1"
        else
            cLbD3="0"
        //alert("click");
        //alert(cLbD2+" "+cLbD3);

        callWSloadBalance(targetcmts, cLbD2,cLbD3)

    });



    $('#btnGetDevices').click(function(){

        //alert("clickDevices");

        callWSgetDevices();


    });




    $('#genDSfreq').click(function(){

        //alert("clickDevices");
        //alert("click DS generate");
        generateDSfs();


    });

});