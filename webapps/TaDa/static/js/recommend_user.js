// Adopted from http://www.webdesigncrowd.com/menu-transition-effects/
$(function() {
 	
 	$('.recommend-user-item').each(function(idx){
	    
	    var fromTop = idx * 200;
	    var delayTime = ((idx+1) * 200) + Math.floor((Math.random() * 200) + 1);

		$(this).css("top", fromTop + 800);
		
   	 	$(this).fadeIn();

	    $(this).delay(delayTime).queue(function(){      	

	   	 	$(this).css("top", fromTop);
	    	$(this).dequeue();
	  	});
	});
	
});


