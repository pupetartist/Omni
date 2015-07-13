$(document).ready(function() {
	 function showResults() {
		  var spinner = $('.glyphicon-spin');
		  spinner.toggleClass('glyphicon-spin');
		  spinner.hide();
		  
		  $('#routes-search-progress').hide();
        
		  $('#routes-header').removeClass('hidden');
		  $('#routes-list').removeClass('hidden');
        $('#route-instructions').removeClass('hidden');
	 }

	 window.setTimeout(showResults, 1500);

	 $('#routes-list li:nth-child(1)').addClass('selected tab');
	 $('#routes-list li').click(function() {
		  $('#routes-list li').removeClass('selected');
		  $(this).addClass('selected tab');
	 });
});
