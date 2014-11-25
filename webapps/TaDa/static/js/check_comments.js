// Customized javascript via jQuery
// $('.notification-icon').on('mouseover', function() {
//      $(this).effect("bounce", {times:2 }, 1000);
// });

$(document).ready( function() {

	checkAjax();
	setInterval(checkAjax, 15000);

});

function checkAjax() {

	// Check only when logged in
	if ( $( "#log-btn" ).attr( "status" ) == "loggedin" ) {

		$.ajax(
		{
			url: "/check-comments",
			type: "GET",
			dataType: "html",
			success:function(html) 
			{
				// alert( "success" );

				if( html ){
					$("#notification").removeClass("notification");
				}
				$('#notification-list').empty();
				$('#notification-list').prepend(html);		    
		
			},
			error: function() 
			{
			    //if fails 
			    // alert( "error" );     
			}
		});

	}
	
}
