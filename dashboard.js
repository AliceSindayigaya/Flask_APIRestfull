(function () {
    isWindows = navigator.platform.indexOf('Win') > -1 ? true : false;

    if (isWindows) {
        //$('.sidebar .sidebar-wrapper, .main-panel, .modal').perfectScrollbar();

        $('html').addClass('perfect-scrollbar-on');
    } else {
        $('html').addClass('perfect-scrollbar-off');
    }
})();

$(document).ready(function () {

    if ($('.full-screen-map').length == 0 && $('.bd-docs').length == 0) {
        // On click navbar-collapse the menu will be white not transparent
        $('.collapse').on('show.bs.collapse', function () {
            $(this).closest('.navbar').removeClass('navbar-transparent').addClass('bg-white');
        }).on('hide.bs.collapse', function () {
            $(this).closest('.navbar').addClass('navbar-transparent').removeClass('bg-white');
        });
    }

    nowuiDashboard.initMinimizeSidebar();

    $navbar = $('.navbar[color-on-scroll]');
    scroll_distance = $navbar.attr('color-on-scroll') || 500;

    // Check if we have the class "navbar-color-on-scroll" then add the function to remove the class "navbar-transparent" so it will transform to a plain color.
    if ($('.navbar[color-on-scroll]').length != 0) {
        nowuiDashboard.checkScrollForTransparentNavbar();
        $(window).on('scroll', nowuiDashboard.checkScrollForTransparentNavbar);
    }

    $('.form-control').on("focus", function () {
        $(this).parent('.input-group').addClass("input-group-focus");
    }).on("blur", function () {
        $(this).parent(".input-group").removeClass("input-group-focus");
    });

    // Activate bootstrapSwitch
    $('.bootstrap-switch').each(function () {
        $this = $(this);
        data_on_label = $this.data('on-label') || '';
        data_off_label = $this.data('off-label') || '';

        $this.bootstrapSwitch({
            onText: data_on_label,
            offText: data_off_label
        });
    });
});

//navbar 
$(document).on('click', '.navbar-toggle', function () {
    $toggle = $(this);

    if (homologate.misc.navbar_menu_visible == 1) {
        $('html').removeClass('nav-open');
        homologate.misc.navbar_menu_visible = 0;
        setTimeout(function () {
            $toggle.removeClass('toggled');
            $('#bodyClick').remove();
        }, 550);
    } else {
        setTimeout(function () {
            $toggle.addClass('toggled');
        }, 580);

        div = '<div id="bodyClick"></div>';
        $(div).appendTo('body').click(function () {
            $('html').removeClass('nav-open');
            homologate.misc.navbar_menu_visible = 0;
            setTimeout(function () {
                $toggle.removeClass('toggled');
                $('#bodyClick').remove();
            }, 550);
        });

        $('html').addClass('nav-open');
        nowuiDashboard.misc.navbar_menu_visible = 1;
    }
});

nowuiDashboard = {
    misc: {
        navbar_menu_visible: 0
    },

    initMinimizeSidebar: function initMinimizeSidebar() {
        if ($('.sidebar-mini').length != 0) {
            sidebar_mini_active = true;
        }

        $('#minimizeSidebar').click(function () {
            var $btn = $(this);

            if (sidebar_mini_active == true) {
                $('body').removeClass('sidebar-mini');
                sidebar_mini_active = false;
                nowuiDashboard.showSidebarMessage('Sidebar mini deactivated...');
            } else {
                $('body').addClass('sidebar-mini');
                sidebar_mini_active = true;
                nowuiDashboard.showSidebarMessage('Sidebar mini activated...');
            }
        });
    },
//Sidebar menu
showSidebarMessage: function showSidebarMessage(message) {
        try {
            $.notify({
                icon: "now-ui-icons ui-1_bell-53",
                message: message
            }, {
                type: 'info',
                timer: 4000,
                placement: {
                    from: 'top',
                    align: 'right'
                }
            });
        } catch (e) {
           // console.log('Notify library is missing, please make sure you have the notifications library added.');
        }
    }

};

hexToRGB = function hexToRGB(hex, alpha) {
    var r = parseInt(hex.slice(1, 3), 16),
        g = parseInt(hex.slice(3, 5), 16),
        b = parseInt(hex.slice(5, 7), 16);

    if (alpha) {
        return "rgba(" + r + ", " + g + ", " + b + ", " + alpha + ")";
    } else {
        return "rgb(" + r + ", " + g + ", " + b + ")";
    }
};
//Get filePath 
function getPath(file){
    var realPath = file_path.replace(/[\/]/g, "\\");
  return realPath;
}

//Show resultat page
function showResult(){
    document.getElementById('resultat').style.display='block';
}
//content API show
    function showApiDga(){
        document.getElementById('bdmodel').style.display='none';
     
    }
    function showApiBdmodel(){
        document.getElementById('bdmodel').style.display='block';
    } 
//Show the content bank moteur
    function showLocal(){

        document.getElementById('projet').style.display='none';
        document.getElementById('locale').style.display='block';
    }
       
    function showProjet(){
    
        document.getElementById('projet').style.display='block';
        document.getElementById('locale').style.display='none';
    } 

    function showtab1(){
        document.getElementById('1').style.display='block';
    }

    function showtab2(){
        document.getElementById('1').style.display='block';
        document.getElementById('2').style.display='block';
    }

    function showtab3(){
        document.getElementById('1').style.display='block';
        document.getElementById('2').style.display='block';
        document.getElementById('3').style.display='block';
    }

    function showtab4(){
        document.getElementById('1').style.display='block';
        document.getElementById('2').style.display='block';
        document.getElementById('3').style.display='block';
        document.getElementById('4').style.display='block';
    }

    function showtab5(){
        document.getElementById('1').style.display='block';
        document.getElementById('2').style.display='block';
        document.getElementById('3').style.display='block';
        document.getElementById('4').style.display='block';
        document.getElementById('5').style.display='block';
    }

//'CONTROL RESULTAT' AND 'CODI' buttons
    $('.custom-file-input').on('change',function(){
    $(this).next('.form-control-file').addClass("selected").html($(this).val());
})
    $('.first a').on('click', function(){    
    $('.first-toggle').html($(this).html());    
})

    $('.second a').on('click', function(){    
    $('.second-toggle').html($(this).html());    
})

//Control the user enter
// Fonction to unable the "tooltips"
function deactivateTooltips() {

    var tooltips = document.querySelectorAll('.tooltip'),
        tooltipsLength = tooltips.length;

    for (var i = 0; i < tooltipsLength; i++) {
        tooltips[i].style.display = 'none';
    }

}
//Get the input tooltips
function getTooltip(elements) {

    while (elements = elements.nextSibling) {
        if (elements.className === 'tooltip') {
            return elements;
        }
    }

    return false;

}

var check= {};

check['api'] =function (){
    var api = document.getElementsByName('api'),
        tooltipStyle = getTooltip(api[1].parentNode).style;
    if(api[0].checked || api[1].checked){
        tooltipStyle.display = 'none';
        return true;
    }else{
        tooltipStyle.display = 'inline-block';
        return false;
    }

};

// //Submit function,( don't control 'CODE RESULTAT' button)*
//form_valid.addEventListener('submit', function(e) {
//        var result = true;
//        for (var i in check) {
//            result = check[i](i) && result;
//       }
//        if (result) {
//           alert('Le formulaire est bien rempli.');
//      }       e.preventDefault();   });

//RAZ button
//form_valid.addEventListener('reset', function() {
//        for (var i = 0; i < inputs.length; i++) {
//            inputs[i].className = '';        }
//        deactivateTooltips();
//    });




//Submit button
$(document).ready(function() {
    $("#buttons").click(function(){
        var select = $('#cresult');
        if (select.val() === ''){
            alert("Veuillez sélectionner le code résultat.");
        }else if (select.val() === '1'){
            document.getElementById('1').style.display='block';
        }
            return false;
      


          });
});

//Check the form

function surligne(champ,error){
    if (error)
        champ.style.backgroundColor = "#fba";
    else
        champ.style.backgroundColor = "";
}

function selectLib(){
    if(document.getElementById("hc").files.length == 0){
        alert('No file selected');
    }
}


function verifinstall(champ){

    if(champ.value.length <3){
        surligne(champ, true);
        return false;
    }
    else

    {
        surligne(champ, false);
        return true;
    }
}

function verifregime(champ){
    if(champ.value.length <3){
        surligne(champ, true);
        return false;
    }
    else
    {
        surligne(champ, false);
        return true;
    }
}
//Check the form content
function verifform(form){
    var install = verifinstall(form.install);
    var regime = verifregime(form.regime);

    if(install && regime)
    {
        return true;
    }else{
        alert("Veuiller remplir correctement, INSTALL, REGIME");
        
        return false;
    }

}
    
//Button fill form
function loadValue() {
        
        document.getElementById ('altitude').value = "15000";
        document.getElementById('mach').value = "0.8";
        document.getElementById('disa').value = "-10";
        document.getElementById('humidite').value = "-10";
        document.getElementById('alt_piste').value = "15000";
        document.getElementById('disa_piste').value = "-10";
        document.getElementById('temps_flex').value = "1";
        document.getElementById('typar').value = "FNI";
        document.getElementById('vapar').value = "0.1";
        document.getElementById('install').value = "005";
        document.getElementById('regime').value = "MCL";
        
        }


//Library checkbox funcion 
function getLibChecked(){
        
        var pathLib = ['path1', 'path2', 'path3','path4'];
        for (var i=0; i < pathLib.length; i++){
                if (document.getElementById("input_"+pathLib[i]).checked){
                        return document.getElementById("input_"+pathLib[i]).value ;
                        }
                }
        }

//Redirect with the result page 
function redirectResult(){
        $('#save_modal').on('click', function(){
                    // var url = "http://caefr0p233:8125/result";
                     document.getElementById('resultat').style.display = 'block';
                     //window.location = url;
                     $('#Modal').modal('hide');
        });
        }



//show result page 
function addResult(data)
	{

    $(document).ready(function(){
      
        var url = "http://caefr0p235:8125/result";
        let resultData = JSON.stringify(data);
        $.ajax({
                "async": true,
                "crossDomain": true,
                type: "POST",
                url:url,
                dataType: "json",
                contentType : "application/json",
                data: resultData,
                success: function(response){
                    //var result = JSON.stringify(response);
                       // console.log(response);
                
                  }
                })
            }); 
	}

// Send the form to the server
$(document).ready(function(){

   $('form').on('submit', function(event){
/*var file = document.getElementById('hc').value;*/
var data = {
    file_path:document.getElementById('hc').value,
    altitude : document.getElementById('altitude').value,
    mach : document.getElementById('mach').value,
    disa: document.getElementById('disa').value,
    humidite: document.getElementById('humidite').value,
    //pathLibrary: getLibChecked(),
    alt_piste: document.getElementById('alt_piste').value,
    disa_piste: document.getElementById('disa_piste').value,
    temps_flex: document.getElementById('temps_flex').value,
    typar: document.getElementById('typar').value,
    vapar: document.getElementById('vapar').value,
    install: document.getElementById('install').value, 
    // flhv: document.getElementById('flhv').value,
   // wbiphp:document.getElementById('wbiphp').value,
    // hpx:document.getElementById('hpx').value,
    regime: document.getElementById('regime').value
    // code_moteur:document.getElementById('code-moteur').value
};
  //console.log(data);

$.ajax({
    "async": true,
    "crossDomain": true,
    type : 'POST',
    url : "http://caefr0p235:8125/sppms/api/v1.0",
    dataType: "html",
    data: data,
    success : function(data){
             //console.log(data);
        
        let alldata = JSON.parse(data);
       console.log(alldata);      
        document.getElementById('ZSPHUM').value = alldata.ZSPHUM;
        document.getElementById('ZPCON').value = alldata.ZPCON;
        document.getElementById('ZFNI').value = alldata.ZFNI;
        document.getElementById('ZFGI').value =  alldata.ZFGI;
        document.getElementById('ZW1A').value = alldata.ZW1A;
        document.getElementById('ZWFE').value = alldata.ZWFE;

        document.getElementById('ZEGT').value =  alldata.ZEGT;
        document.getElementById('ZPNL').value = alldata.ZPNL;
        document.getElementById('ZPNH').value = alldata.ZPNH;
        document.getElementById('ZPS3').value =  alldata.ZPS3;
        document.getElementById('ZPTF').value = alldata.ZPTF;
        document.getElementById('ZPTP').value = alldata.ZPTP;

        document.getElementById('ZW25').value =  alldata.ZW25;
        document.getElementById('ZPT3').value = alldata.ZPT3;
        document.getElementById('ZPED').value = alldata.ZPED;
        document.getElementById('ZPEF').value =  alldata.ZPEF;
        document.getElementById('ZPEH').value = alldata.ZPEH;
        document.getElementById('ZPEI').value = alldata.ZPEI;

        document.getElementById('ZP8M').value =  alldata.ZP8M;
        document.getElementById('ZVEJ').value =  alldata.ZVEJ;
        document.getElementById('ZWBINS').value = alldata.ZWBINS;
        document.getElementById('ZPCONR').value = alldata.ZPCONR;
        document.getElementById('ZFNIR').value =  alldata.ZFNIR;
        document.getElementById('ZFGIR').value = alldata.ZFGIR;
        document.getElementById('ZW1AR').value = alldata.ZW1AR;

        document.getElementById('ZWFER').value =  alldata.ZWFER;
        document.getElementById('ZEGTR').value = alldata.ZEGTR;
        document.getElementById('ZPNLR').value = alldata.ZPNLR;
        document.getElementById('ZPNHR').value =  alldata.ZPNHR;
        document.getElementById('ZEPS').value = alldata.ZEPS;
        document.getElementById('ZTTF').value = alldata.ZTTF;

        document.getElementById('ZTTP').value =  alldata.ZTTP;
        document.getElementById('ZT25').value = alldata.ZT25;
        document.getElementById('ZTT3').value = alldata.ZTT3;
        document.getElementById('ZTED').value =  alldata.ZTED;
        document.getElementById('ZTEF').value = alldata.ZTEF;
        document.getElementById('ZTEH').value = alldata.ZTEH;

        document.getElementById('ZTEI').value =  alldata.ZTEI;
        document.getElementById('ZT8M').value = alldata.ZT8M;
        //document.getElementById('IR').value = alldata.IR;
        document.getElementById('ZPNI').value =  alldata.ZPNI;
        document.getElementById('ZP1A').value = alldata.ZP1A;
        document.getElementById('ZP41').value = alldata.ZP41;

        document.getElementById('ZP5').value =  alldata.ZP5;
        document.getElementById('ZP8').value = alldata.ZP8;
        document.getElementById('ZP18').value = alldata.ZP18;
        document.getElementById('ZPS5').value =  alldata.ZPS5;
        document.getElementById('ZV9').value = alldata.ZV9;
        document.getElementById('ZV19').value = alldata.ZV19;

        document.getElementById('ZAE8').value =  alldata.ZAE8;
        document.getElementById('ZAE18').value = alldata.ZAE18;
        document.getElementById('ZEPMIX').value = alldata.ZEPMIX;
        document.getElementById('ZECO2').value =  alldata.ZECO2;
        document.getElementById('ZESO2').value = alldata.ZESO2;
        document.getElementById('ZEH2O').value = alldata.ZEH2O;

        document.getElementById('ZECO').value =  alldata.ZECO;
        document.getElementById('ZEHC').value = alldata.ZEHC;
        document.getElementById('ZENOX').value = alldata.ZENOX;
        document.getElementById('ZPNIR').value =  alldata.ZPNIR;
        document.getElementById('ZT1A').value = alldata.ZT1A;
        document.getElementById('ZT41').value = alldata.ZT41;

        document.getElementById('ZT5').value =  alldata.ZT5;
        document.getElementById('ZT8').value = alldata.ZT8;
        document.getElementById('ZT18').value = alldata.ZT18;
        document.getElementById('ZT13').value =  alldata.ZT13;
        document.getElementById('ZV9M').value = alldata.ZV9M;
                               
        document.getElementById('ZAE8M').value = alldata.ZAE8M;

        document.getElementById('ZW3').value =  alldata.ZW3;
        document.getElementById('ZW8').value = alldata.ZW8;
        document.getElementById('ZW18').value = alldata.ZW18;
        document.getElementById('ZOUT1').value =  alldata.ZOUT1;
        document.getElementById('ZOUT2').value = alldata.ZOUT2;
        document.getElementById('ZOUT3').value = alldata.ZOUT3;

        document.getElementById('ZOUT4').value = alldata.ZOUT4;
        document.getElementById('ZOUT5').value = alldata.ZOUT5;
       // document.getElementById('VERSION').value = alldata.VERSION;
    
                     
       addResult(alldata);
    }
    
});
    return false
    event.preventDefault();
});
});

//Auto complet alt_piste and disa_piste
$("#altitude").keyup(function(){
        $("#alt_piste").val(this.value);
        });
$("#disa").keyup(function(){
        $("#disa_piste").val(this.value)
        });

//Preloader
//var overlay = document.getElementById("overlay");

//window.addEventListenner('load',function(){
  //      overlay.style.display ='none';
        
   //     });

//function test banque moteur
     var items = [
            {

             aircraft:[], 
             version: [],
             repere: []
             },
            {
             aircraft: [
                     {'name': 'A300', value: 'a300'},
                     {'name': 'A300-600', value: 'a300-600'},
                     {'name': 'A30X',value: 'a30x'},
                     {'name': 'A310', value: 'a310'},
                     {'name': 'A318', value: 'a318'},
                     {'name': 'A319', value: 'a319'},
                     {'name': 'A320', value: 'a320'},
                     {'name': 'A321', value: 'a321'},
                     {'name': 'A330', value: 'a330'},
                     {'name': 'A330ST', value: 'a330ST'}
                     ]
                    },
            {
            version : [
                    {'name': 'A300B2-320', value:'a300B2-320'},
                    {'name': 'A300B4-203', value: 'a300B4-203'}
                    
                    ]
                    
                    },
            {
            repere: [
                    {'name': '01/08/80', value: '01/08/80'},
                    {'name': '01/09/81', value: '01/09/81'},
                    {'name':'09/05/96', value: '09/05/96'}
                    ]
                    }
                
             
                ]

function testBanqueMoteur () {
     
        var temp = {};
         $.each(items, function (){
                 $("")
                 });
        
        }


    
