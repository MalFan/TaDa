// Customized javascript via jQuery
$(document).ready( function() {

	addCommentAjax();

	dislikeAjax();

	setInterval(refreshAjax, 15000);

});


function addCommentAjax() {
	$(".form-comment").submit( function( e ) {

		var postData = $(this).serializeArray();
		var formURL = $(this).attr("action");
		var id = $( this ).attr( "grumbl-id" );
		$.ajax(
		{
			url : formURL,
			type: "POST",
			data : postData,
			success:function(comment) 
			{
				// alert( "success" + id );

				// new hr
				var hr = $( "<hr class=\"comment-hr\">" );

				var currentUsername = $( "li.dropdown a" ).find( "span.current-username" ).html();		

				// new comment div
            		var divPostComments = $( "<div class=\"post-comments\"></div>" );
            		var divPostTitle = $( "<div class=\"post-title\"></div>" );
				var divPostContent = $( "<div class=\"post-content\"></div>" );
				divPostComments.append( divPostTitle );
				divPostComments.append( divPostContent );

				var divPostAvatar = $( "<div class=\"post-avatar\"></div>" );
				var divPostUser = $( "<div class=\"post-user\"></div>" );
				divPostTitle.append( divPostAvatar );
				divPostTitle.append( divPostUser );

				var imgHref = $( "<a/>", { href: "/profile/" + comment[0].fields.user } );
				divPostAvatar.append( imgHref );
				imgHref.append( $( "<img>", { 
					src: "/get-photo/" + currentUsername,
					alt: currentUsername,
					width: "64px"
				} ) );
				divPostUser.append( "<p class=\"grumblr-name\">" + currentUsername + "</p>" );
				divPostUser.append( "<p>" + comment[0].fields.pub_time + "</p>" );
				divPostContent.append( "<p>" + comment[0].fields.text + "</p>" )

				// Append new comment.
				$( "div.post-write-comment[grumbl-id=" + id + "]" ).after( divPostComments );
				$( "div.post-write-comment[grumbl-id=" + id + "]" ).after( hr );

				// Change the reply count.
				$( "form[grumbl-id=" + id + "] input[name='grumbl_comment']" ).val( "" );
				var currentText = $( "a.reply-btn[grumbl-id=" + id + "]" ).children().last().html();
				var currentReplys = currentText.substring(currentText.indexOf("(") + 1, currentText.indexOf(")"))
				var newReplys = parseInt(currentReplys, 10) + 1;
				var newText = current_text.replace(currentReplys, newReplys);
				$( "a.reply-btn[grumbl-id=" + id + "]" ).children().last().html( newText );			    
			},
			error: function() 
			{
				//if fails
				alert( "error" );      
			}
		});
		e.preventDefault(); //STOP default action
	});

}


function dislikeAjax() {
	$( "a.dislike-btn" ).click(function(e) {	
		var id = $( this ).attr( "grumbl-id" );
		var btnHref = "/dislike/" + id
		$.ajax(
		{
			url: btnHref,
			success:function(response) 
			{
				// alert( "success" );

				var currentText = $( "a.dislike-btn[grumbl-id=" + id + "]" ).children().last().html();
				var currentDislikes = currentText.substring(currentText.indexOf("(") + 1, currentText.indexOf(")"))
				
				// alert( current_dislikes );
				var newDislikes = parseInt(currentDislikes, 10) + parseInt(response, 10);
				// alert( new_dislikes );
				var newText = currentText.replace(currentDislikes, newDislikes);
				$( "a.dislike-btn[grumbl-id=" + id + "]" ).children().last().html( newText );
					
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


function refreshAjax() {
	var newestGrumbl = $( 'div.grumbl-main' ).first()
	var newestID = newestGrumbl.attr( 'grumbl-id' )
	if (newestID == null) {
		// alert( "no grumbls" );
		newestID = 0;
	}
	var currentUsername = $( "li.dropdown a" ).find( "span.current-username" ).html();	

	$.ajax(
	{
		url: "refresh",
		type: "GET",
		data: { grumblid: newestID, username: currentUsername },
		success:function(newGrumblsUsers) 
		{
			// alert( "success" );
            		for (var i = 0; i < newGrumblsUsers.length; i += 2) {
				var divPostBox = $( "<div class=\"postbox grumbl-main\" grumbl-id=" + newGrumblsUsers[i].pk + "></div>" );
				var divPostTitle = $( "<div class=\"post-title\"></div>" );
				var divPostContent = $( "<div class=\"post-content\"></div>" );
				divPostBox.append( divPostTitle );
				divPostBox.append( divPostContent );

				var divPostAvatar = $( "<div class=\"post-avatar\"></div>" );
				var divPostUser= $( "<div class=\"post-user\"></div>" );
				divPostTitle.append( divPostAvatar );
				divPostTitle.append( divPostUser );

				var imgHref = $( "<a/>", { href: "/profile/" + newGrumblsUsers[i].fields.user } );
				divPostAvatar.append( imgHref );
				imgHref.append( $( "<img>", { 
					src: "/get-photo/" + newGrumblsUsers[i+1].fields.username,
					alt: newGrumblsUsers[i+1].fields.username,
					width: "64px"
				} ) );

				divPostUser.append( "<p class=\"grumblr-name\">" + newGrumblsUsers[i+1].fields.username + "</p>" );
				divPostUser.append( "<p>" + newGrumblsUsers[i].fields.pub_time + "</p>" );
				divPostContent.append( "<p>" + newGrumblsUsers[i].fields.text + "</p>" )

				if (newGrumblsUsers[i].fields.picture.length != 0) {
					var divPostPicture = $( "<div class=\"post-picture\"></div>" );
					divPostBox.append( divPostPicture );
					divPostPicture.append( $( "<img>", { 
						src: "/get-picture/" + newGrumblsUsers[i].pk,
						width: "100%"
					} ) );
				}

				// Append new grumbl.
				$( 'div.grumblebox' ).after( divPostBox );
	          }
	
		},
		error: function() 
		{
		    //if fails 
		    // alert( "error" );     
		}
	});
	
}