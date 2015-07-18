$(document).ready(function() {
    $("ul:eq(0) li").click(function(){
    	var img = $(this).attr("id").substring(3);
    	if(!$(this).hasClass("active")){
	    	$(this).addClass("active");
	    	$(this).find("img").attr('src',('../static/img/genericos/'+img+'_on.png'));
    	}else{
    		$(this).removeClass("active");
	    	$(this).find("img").attr('src',('../static/img/genericos/'+img+'_off.png'));
    	}
    });
});