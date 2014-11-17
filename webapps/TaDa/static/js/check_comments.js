// Customized javascript via jQuery
// $('.notification-icon').on('mouseover', function() {
//      $(this).effect("bounce", {times:2 }, 1000);
// });

$(document).ready( function() {

	setInterval(checkAjax, 15000);

});

function checkAjax() {

	// Check only when logged in
	if ( $( "#log-btn" ).attr( "status" ) == "loggedin" ) {

		$.ajax(
		{
			url: "/check-comments",
			type: "GET",
			success:function(reviews) 
			{
				// alert( "success" );
				// var ids;
				if(reviews.length > 0){
					$("#notification").removeClass("notification");
				}
				for (var i = 0; i < reviews.length; i += 1) {
					// ids += reviews[i].pk
					// ids += "; "
					console.log(reviews[i].pk);
					console.log(reviews[i].fields.title);
				}
				// alert( ids );
		
			},
			error: function() 
			{
			    //if fails 
			    // alert( "error" );     
			}
		});

	}
	
}
