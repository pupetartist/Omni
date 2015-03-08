

function init_map2() {

var myOptions = {
    zoom: 14,
    center: new google.maps.LatLng(19.43270,-99.13412),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }

 var map2 = new google.maps.Map(
 document.getElementById('mapa'),myOptions);
}

$(window).load(init_map2);

    