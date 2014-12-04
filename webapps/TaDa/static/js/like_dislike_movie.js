// Customized javascript via jQuery
$(document).ready( function() {

	likeAjax();
	dislikeAjax();

});

function likeAjax() {
	$( "#like-btn" ).click(function(e) {
		if(isLogin()){
			var btnHref = $( this ).attr( "href" );
			$.ajax(
			{
				url: btnHref,
				success:function(response) 
				{
					var currentLikes = $( "#like-badge-span" ).html();
					
					var newLikes = parseInt(currentLikes, 10) + parseInt(response, 10);
					$( "#like-badge-span" ).html( newLikes );
					if ( response == "1" ) {
						$( "#like-btn" ).removeClass( "btn-default" ).addClass( "btn-info" );
						$( "#like-text-span" ).html( "Unlike" );
						$( "#like-btn" ).attr("status", "liked");
						var dislikeBtn = $( "#dislike-btn" );
						if(dislikeBtn.attr("status") == "disliked"){
							$( "#dislike-btn" ).removeClass( "btn-info" ).addClass( "btn-default" );
							$( "#dislike-text-span" ).html( "Dislike" );
							$( "#dislike-btn" ).removeAttr("status");
							var currentDislikes = parseInt($( "#dislike-badge-span" ).html());
							var newDislikes = currentDislikes - 1;
							$( "#dislike-badge-span" ).html((newDislikes).toString());
						}
					} else {
						$( "#like-btn" ).removeClass( "btn-info" ).addClass( "btn-default" );
						$( "#like-text-span" ).html( "Like" );
						$( "#like-btn" ).removeAttr("status");
					}
						
				},
				error: function() 
				{  
				}
			});			
		}else{
			$('.login-popup').modal();
		}
		e.preventDefault(); //STOP default action
	});
}

function dislikeAjax() {
	$( "#dislike-btn" ).click(function(e) {	
		if(isLogin()){
			var btnHref = $( this ).attr( "href" );
			$.ajax(
			{
				url: btnHref,
				success:function(response) 
				{
					var currentDislikes = $( "#dislike-badge-span" ).html();
					var newDislikes = parseInt(currentDislikes, 10) + parseInt(response, 10);
					$( "#dislike-badge-span" ).html( newDislikes );
					if ( response == "1" ) {
						$( "#dislike-btn" ).removeClass( "btn-default" ).addClass( "btn-info" );
						$( "#dislike-text-span" ).html( "Undislike" );
						$( "#dislike-btn" ).attr("status", "disliked");
						var likeBtn = $( "#like-btn" );
						if(likeBtn.attr("status") == "liked"){
							$( "#like-btn" ).removeClass( "btn-info" ).addClass( "btn-default" );
							$( "#like-text-span" ).html( "Like" );
							$( "#like-btn" ).removeAttr("status");
							var currentLikes = parseInt($( "#like-badge-span" ).html());
							var newLikes = currentLikes - 1;
							$( "#like-badge-span" ).html((newLikes).toString());
						}
					} else {
						$( "#dislike-btn" ).removeClass( "btn-info" ).addClass( "btn-default" );
						$( "#dislike-text-span" ).html( "Dislike" );
						$( "#dislike-btn" ).removeAttr("status");
					}
				},
				error: function() 
				{   
				}
			});
		}else{
			$('.login-popup').modal();
		}
		e.preventDefault(); //STOP default action
	});
}

function isLogin(){
	var status = $("#log-btn").attr("status");
	if(status == "loggedin"){
		return true;
	}else{
		return false;
	}
}
