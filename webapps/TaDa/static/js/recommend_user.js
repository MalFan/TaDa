$(function() {
 	
 	$('.recommend-user-item').each(function(idx){
	    
	    var fromTop = idx * 150;
	    var delayTime = ((idx+1) * 200) + Math.floor((Math.random() * 200) + 1);

		$(this).css("top", fromTop + 800);
		
   	 	$(this).fadeIn();

	    $(this).delay(delayTime).queue(function(){      	

	   	 	$(this).css("top", fromTop);
	    	$(this).dequeue();
	  	});
	});
	
});


