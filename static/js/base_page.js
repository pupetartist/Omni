var mexico_city_center = new google.maps.LatLng(19.432845, -99.133259);
var naucalpan_center = new google.maps.LatLng(19.473081, -99.243303);

var mexico_city_bounds = new google.maps.LatLngBounds(
	 new google.maps.LatLng(19.1906, -99.5622), // SW
	 new google.maps.LatLng(19.6743, -98.7039) // NE
);

$(document).ready(function() {
	 var current_location_circle = null;
	 var origin_marker = null;
	 var destination_marker = null;
	 var map = $('#map-canvas');
	 
	 function is_enabled(selector) {
		  return !$(selector).prop('disabled');
	 }
	 
	 function disable_elements(selector) {
		  $(selector).prop('disabled', true);
	 }

	 function enable_elements(selector) {
		  $(selector).prop('disabled', false);
	 }

	 function disable_form_controls() {
		  disable_elements('#search input[type=text]');
		  disable_elements('#search button');
	 }

	 function enable_form_controls() {
		  enable_elements('#search input[type=text]');
		  enable_elements('#search button');
	 }

	 function toggleSpinner(hide_element_selector, spinner_sector) {
		  $(hide_element_selector).toggleClass('hidden');
		  var spinner = $(spinner_sector);
		  spinner.toggleClass('glyphicon-spin');
		  spinner.toggleClass('hidden');
	 }

	 function toggleSearchControls(id) {
		  if (is_enabled('#' + id))
				disable_form_controls();
		  else
				enable_form_controls();
		  toggleSpinner('#' + id + '-icon', '#' + id + '-spinner');
	 }

	 function ensure_map_is_visible(after_action) {
		  if (map.hasClass('hidden')) {
				map.removeClass('hidden', 300, 'easeOutCubic', function() {
					 map.gmap('option', 'center', mexico_city_center);
					 map.gmap('refresh');
					 if (after_action)
						  after_action();
				});
		  }
		  else if (after_action) {
				after_action();
		  }
	 }

	 function add_autocomplete(id) {
		  var options = {
				bounds: mexico_city_bounds,
				componentRestrictions: {country: 'mx'},
				types: ['geocode']
		  };
		  var autocomplete = new google.maps.places.Autocomplete(
				$(to_selector(id))[0], options);
	 }

	 function add_marker(location, icon, input_binding_id) {
		  var marker = map.gmap('addMarker', {
				'position': location,
				'draggable': true,
				'icon': icon
		  });
		  google.maps.event.addListener(
				marker[0], 'dragend', function() 
				{
					 geocodePosition(marker[0].getPosition(), function(address) {
						  $(input_binding_id).val(address);
					 });
				});
		  // marker is a jQuery wrapper, but we just want the DOM element
		  return marker[0];
	 }

	 function delete_marker(marker) {
		  if (marker != null) {
				marker.setMap(null);
		  }
	 }

	 function add_circle(location, radius) {
		  var circle = map.gmap('addShape', 'Circle', { 
				'strokeWeight': 0, 
				'fillColor': "#008595",
				'fillOpacity': 0.25, 
				'center': location, 
				'radius': radius, 
				'clickable': false 
		  });
		  // circle is a jQuery wrapper, but we just want the DOM element
		  return circle[0];
	 }

	 function delete_circle(circle) {
		  if (circle != null) {
				circle.setMap(null);
		  }
	 }
	 
	 function set_marker(marker, location, icon, input_binding_id) {
		  delete_marker(marker);
		  var marker = add_marker(location, icon, input_binding_id);
		  return marker;
	 }
	 
	 function set_origin_marker(location) {
		  origin_marker = set_marker(
				origin_marker, location, '/static/img/origin-icon.png', '#origin');
	 }

	 function set_destination_marker(location) {
		  destination_marker = set_marker(
				destination_marker, location, '/static/img/destination-icon.png', '#destination');
	 }

	 function zoom_to_street_level(geolocation) {
		  map.gmap('option', 'zoom', 16);
		  map.gmap('option', 'center', geolocation);
		  map.gmap('refresh');
	 }
	 
	 function locate_on_map(id, set_marker, after_action) {
		  var address = $(to_selector(id)).val();
		  if (address) {
				toggleSearchControls(id);
				geolocate_address(address, function(location) {
					 ensure_map_is_visible(function() {
						  toggleSearchControls(id);
						  
						  set_marker(location);
						  map.gmap('option', 'center', location);
						  zoom_to_street_level();
						  
						  after_action();
					 });
				}, function() {
					 toggleSearchControls(id);
					 alert('No pudimos localizar esa dirección. Intenta ser más específico.');
				});
		  }
	 }
	 
	 function add_current_location_circle(geolocation, accuracy_in_m) {
		  delete_circle(current_location_circle);
		  current_location_circle = add_circle(geolocation, accuracy_in_m);
	 }

	 function results_in_mexico_city(geolocate_results) {
		  return geolocate_results;
	 }
	 
	 function geolocate_address(address, successAction, failAction) {
		  var geocoder = new google.maps.Geocoder();
		  geocoder.geocode({ 'address': address}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					 if (successAction) {
						  results = results_in_mexico_city(results);
						  if (results.length > 0)
								successAction(results[0].geometry.location);
					 }
				} else {
					 if (failAction)
						  failAction(status);
				}
		  });
	 }

	 function geocodePosition(pos, successAction, failAction)
	 {
		  var geocoder = new google.maps.Geocoder();
		  geocoder.geocode(
				{
					 latLng: pos
				}, 
				function(results, status) 
				{
					 if (status == google.maps.GeocoderStatus.OK) 
					 {
						  if (successAction)
								successAction(results[0].formatted_address);
					 }
					 else if (failAction) {
						  failAction(status);
					 }
				}
		  );
	 }
	 
	 function update_find_me_view(position, address) {
		  var geolocation = new google.maps.LatLng(
				position.coords.latitude, position.coords.longitude);

		  ensure_map_is_visible(function() {
				$('#origin').val(address);
				set_origin_marker(geolocation);
				add_current_location_circle(geolocation, position.coords.accuracy);
				zoom_to_street_level(geolocation);
				toggleSearchControls('find-me');
				$('#destination').focus();
		  });
	 }
	 
	 function geolocate() {
		  if (navigator.geolocation) {
				toggleSearchControls('find-me');
				$('#origin').val('Buscando tu ubicación...');
				
				navigator.geolocation.getCurrentPosition(
					 function(position) {
						  var geolocation = new google.maps.LatLng(
								position.coords.latitude, position.coords.longitude);
						  
						  geocodePosition(geolocation, function(address) {
								update_find_me_view(position, address);
								
						  }, function() {
								var address = position.coords.latitude + '' + position.coords.longitude;
								update_find_me_view(position, address);
						  });
					 },
					 function() {
						  toggleSearchControls('find-me');
						  $('#origin').val('Lo sentimos, no pudimos encontrar tu ubicación automáticamente.');
						  $('#find-me').focus();
					 },
					 {
						  enableHighAccuracy: false,
						  /* TODO: What's the right timeout to strike a balance between accuracy and usability? */
						  timeout: 10 * 1000, /* ms == 10 seconds */
						  maximumAge: 60 * 1000 /* ms == 60 seconds */
					 });
		  } else {
				// TODO: replace with a more user-friendly dialog (not necessarily modal)
				alert('Lo sentimos, tu navegador no parece soportar geolocalización. Considera actualizarlo.');
		  }
	 }

	 function on_enter(selector, action) {
		  $(selector).on("keyup keypress", function(e) {
				var code = e.keyCode || e.which; 
				if (code  == 13) {
					 e.preventDefault();
					 if (action)
						  action(e);
					 return false;
				}
		  });
	 }

	 function to_selector(id) {
		  return '#' + id;
	 }
	 
	 function locate_on_enter(id, set_marker_fn, after_action) {
		  on_enter(to_selector(id), function(e) {
				locate_on_map(id, set_marker_fn, after_action);
		  });
	 }

	 function locate_on_click(id, input_id, set_marker_fn, after_action) {
		  $(to_selector(id)).click(function() {
				locate_on_map(input_id, set_marker_fn, after_action);
		  });
	 }

	 function make_focus_on(selector) {
		  return function() {
				$(selector).focus();
		  };
	 }
	 
	 $('#find-me').click(function() {
		  geolocate();
	 });

	 add_autocomplete('origin');
	 add_autocomplete('destination');

	 var focus_on = make_focus_on('#destination');
	 locate_on_enter('origin', set_origin_marker, focus_on);
	 locate_on_click('locate-origin-btn', 'origin', set_origin_marker, focus_on);

	 focus_on = make_focus_on('#search-btn');
	 locate_on_enter('destination', set_destination_marker, focus_on);
	 locate_on_click('locate-destination-btn', 'destination', set_destination_marker, focus_on);
	 
	 $('#origin').focus();
});

function init_map() {
	 var map = new google.maps.Map(
		  document.getElementById('map-canvas'));
}

$(window).load(init_map);
