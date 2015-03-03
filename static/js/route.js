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

	 function configureTimers() {
		  $('.dial').knob({
				'max': 60,
				'readOnly': true,
				'width': 70,
				'height': 70,
				'fgColor': '#009ADE',
				
				/* This is a workaround for issue: #214 & #223 on jQuery-Knob 
				 * https://github.com/aterrien/jQuery-Knob/issues/214
				 * https://github.com/aterrien/jQuery-Knob/issues/223
				 */
				'inline': false, 
				'format': function(v) { return sprintf('%d min', v); },
				'thickness': 0.25,
				'inputColor': 'black'
		  });
	 }

	 window.setTimeout(showResults, 1500);
	 configureTimers();

	 $('#routes-list li:nth-child(1)').addClass('selected tab');
	 $('#routes-list li').click(function() {
		  $('#routes-list li').removeClass('selected');
		  $(this).addClass('selected tab');
	 });
});
