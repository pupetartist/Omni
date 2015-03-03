$(document).ready(function() {
	 $('#origin').focus();
	 
	 $('#find-me').click(function() {
		  alert('Locating your position...');
		  $('#origin').val('Dulce Maguey, Cozumel, Cuauhtémoc, Ciudad de México, DF');
		  $('#destination').focus();
	 });
});
