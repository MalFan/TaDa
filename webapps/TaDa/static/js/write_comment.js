// Customized javascript via jQuery
$(document).ready( function() {

	writeCommentAjax();

});


function writeCommentAjax() {
	$("#review-form").submit( function( e ) {
		var postData = $(this).serializeArray();
		var formURL = $(this).attr("action");
		$.ajax(
		{
			url : formURL,
			type: "POST",
			data : postData,
			dataType: "html",
			success:function(html) 
			{
				// alert( "success" );
				$('ul.comment-list').prepend(html);		    
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

