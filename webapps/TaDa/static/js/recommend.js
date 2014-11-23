$(function() {
 	var window_width = $(window).width();
 	var number_in_row = 5;
 	if(window_width < 1200 && window_width >= 992){
 		number_in_row = 4;
 	}else if(window_width < 992){
		number_in_row = 3;
 	}
 	$('.flip-container').each(function(idx){
	    
	    var row_i = Math.floor(idx / number_in_row); // Vertical Index
	    var col_i = idx % number_in_row; // Horizontal Index
	    var fromTop = row_i * 317;
	    var fromLeft = col_i * 214;
	    var delayTime = ((row_i+1) * 100) + Math.floor((Math.random() * 100) + 1);

		$(this).css("left", fromLeft);
		$(this).css("top", fromTop + 800);
		
   	 	$(this).fadeIn();

	    $(this).delay(delayTime).queue(function(){      	

	   	 	$(this).css("top", fromTop);
	    	$(this).dequeue();
	  	});
	});
	
});


