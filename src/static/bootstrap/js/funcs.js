/**
 * Created by waltergomez on 4/5/17.
 */



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
            '<option value="1">TDMA</option>' +
            '<option value="2">ATDMA</option>' +
            '<option value="3">QPSK</option> ' +
            '</select></li>';

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
