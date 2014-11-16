// Customized javascript via jQuery
$(document).ready( function() {

	likeAjax();
	dislikeAjax();

});

function likeAjax() {
	$( "#like-btn" ).click(function(e) {	
		var btnHref = $( this ).attr( "href" );
		$.ajax(
		{
			url: btnHref,
			success:function(response) 
			{
				// alert( "success" );
				var currentLikes = $( "#like-badge-span" ).html();
				var newLikes = parseInt(currentLikes, 10) + parseInt(response, 10);
				$( "#like-badge-span" ).html( newLikes );
				if ( response == "1" ) {
					$( "#like-btn" ).removeClass( "btn-default" ).addClass( "btn-info" );
					$( "#like-text-span" ).html( "Unlike" );
				} else {
					$( "#like-btn" ).removeClass( "btn-info" ).addClass( "btn-default" );
					$( "#like-text-span" ).html( "Like" );
				}
					
			},
			error: function() 
			{
			    //if fails 
			    // alert( "error" );     
			}
		});
		e.preventDefault(); //STOP default action
	});
}

function dislikeAjax() {
	$( "#dislike-btn" ).click(function(e) {	
		var btnHref = $( this ).attr( "href" );
		$.ajax(
		{
			url: btnHref,
			success:function(response) 
			{
				// alert( "success" );
				var currentDislikes = $( "#dislike-badge-span" ).html();
				var newDislikes = parseInt(currentDislikes, 10) + parseInt(response, 10);
				$( "#dislike-badge-span" ).html( newDislikes );
				if ( response == "1" ) {
					$( "#dislike-btn" ).removeClass( "btn-default" ).addClass( "btn-info" );
					$( "#dislike-text-span" ).html( "Undislike" );
				} else {
					$( "#dislike-btn" ).removeClass( "btn-info" ).addClass( "btn-default" );
					$( "#dislike-text-span" ).html( "Dislike" )
				}
			},
			error: function() 
			{
			    //if fails 
			    // alert( "error" );     
			}
		});
		e.preventDefault(); //STOP default action
	});
}

