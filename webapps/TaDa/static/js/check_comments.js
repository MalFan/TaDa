// Customized javascript via jQuery
$('.notification-icon').on('mouseover', function() {
     $(this).effect("bounce", {times:2 }, 1000);
});

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
				var ids;
				for (var i = 0; i < reviews.length; i += 1) {
					ids += reviews[i].pk
					ids += "; "
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
