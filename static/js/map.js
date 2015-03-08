$(window).load(function() {
    var map1 = L.map('map1').setView([19.35715, -99.08226], 12);

    L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'examples.map-i875mjb7'
    }).addTo(map1);

    // L.marker([19.43270,-99.13412])
    //     .addTo(map)
    //     .bindPopup("<b>Inicio </b><br />Mi primera ruta.").openPopup();

    // function onMapClick(e) {
    //     var popup = L.popup();
    //     popup
    //         .setLatLng(e.latlng)
    //         .setContent("Hiciste click en " + e.latlng.toString())
    //         .openOn(map);
    // }

    // map.on('click', onMapClick);

    function onEachFeature(feature, layer) {
        var popupContent = "";
        if (feature.properties && feature.properties['name']) {
            popupContent += "Estacion: " + feature.properties['name'];
         }
        layer.bindPopup(popupContent);
    }

	 $("#search-form").submit(function(event) {
		  event.preventDefault();
	 });

	 L.geoJson(rutas, {
		  style: function (feature) {
				return feature.properties && feature.properties.style;
		  },

		  onEachFeature: onEachFeature,

		  pointToLayer: function (feature, latlng) {
				return L.circleMarker(latlng, {
					 radius: 4,
					 fillColor: "#ff7800",
					 color: "#000",
					 weight: 1,
					 opacity: 1,
					 fillOpacity: 0.8
				});
		  }
	 }).addTo(map1);
	 
	 
	 $('#search-route').click(function() {
		  $.getJSON('/search.json?origin=Tacuba&destination=Balderas', function(data) {
				
				var routes = data['content']['route_nodes'];

//otra layer para los micros

L.geoJson(micros, {
		  style: function (feature) {
				return feature.properties && feature.properties.style;
		  },

		  onEachFeature: onEachFeature,

		  pointToLayer: function (feature, latlng) {
				return L.circleMarker(latlng, {
					 radius: 4,
					 fillColor: "#f47800",
					 color: "#000",
					 weight: 1,
					 opacity: 1,
					 fillOpacity: 0.8
				});
		  }
	 }).addTo(map1);


				// $('body').append(routes);
				
///comentado por comodidad
				//L.geoJson(routes, {
				//	 style: function (feature) {
//						  return feature.properties && feature.properties.style;
//					 },
//
//					 onEachFeature: onEachFeature,
//
//					 pointToLayer: function (feature, latlng) {
//						  return L.circleMarker(latlng, {
//								radius: 4,
//								fillColor: "#ff7800",
//								color: "#000",
//								weight: 1,
//								opacity: 1,
//								fillOpacity: 0.8
//						  });
//					 }
//				}).addTo(map1);
			  });
	 });
});

