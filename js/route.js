function showResults() {
	 var spinner = $('.glyphicon-spin');
	 spinner.toggleClass('glyphicon-spin');
	 spinner.hide();
	 
	 $('#routes-header').toggleClass('hidden');
	 $('#routes-list').toggleClass('hidden');
}

$(document).ready(function() {
	 window.setTimeout(showResults, 700);
	 $('#destination').focus();
});
