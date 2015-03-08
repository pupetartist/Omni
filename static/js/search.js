$(window).load(function() {
    var map = L.map('map').setView([19.43270,-99.13412], 13);

    L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'examples.map-i875mjb7'
    }).addTo(map);

    L.marker([19.43270,-99.13412])
        .addTo(map)
        .bindPopup("<b>Inicio </b><br />Mi primera ruta.").openPopup();

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
        if (feature.properties && feature.properties.name) {
            popupContent += "Estacion: " + feature.properties.name;
        }
        layer.bindPopup(popupContent);
    }

    L.geoJson(rutas, {
        style: function (feature) {
            return feature.properties && feature.properties.style;
        },

        onEachFeature: onEachFeature,

        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, {
                radius: 7,
                fillColor: "#ff7800",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            });
        }
    }).addTo(map);

	 $('#search-route').click(function() {
	 });
});

