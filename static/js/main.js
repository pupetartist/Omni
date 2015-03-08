

//function init_map2() {


//
//var myOptions = {
//    zoom: 14,
//   center: new google.maps.LatLng(19.43270,-99.13412),
//    mapTypeId: google.maps.MapTypeId.ROADMAP
// }


//var map2 = new google.maps.Map(
// document.getElementById('mapa'),myOptions);
//}


//$(window).load(init_map2);


var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];

function initmap() {
  // set up the map
  map = new L.Map('map');

  // create the tile layer with correct attribution
  var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
  var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 12, attribution: osmAttrib});   

  // start the map in South-East England
  map.setView(new L.LatLng(51.3, 0.7),9);
  map.addLayer(osm);
}

