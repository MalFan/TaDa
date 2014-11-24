// Customized javascript via jQuery
$(document).ready( function() {

	writeCommentAjax();

});


function writeCommentAjax() {
	$("#review-form").submit( function( e ) {
		if(isLogin()){
			var input = $("#id_text")
			var content = input.val();
			console.log(content);
			if (!content.trim()) {
	        // is empty or whitespace
			  input.attr("placeholder","Cannot post an empty comment.")
			  input.attr("class","form-control input_warning")
			}else{
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
				 //STOP default action
				input.removeAttr("placeholder")
			  	input.removeAttr('value'); 
			  	input.attr("class","form-control")         
			  	input.val('');
			}
		}else{
			$('.login-popup').modal();
		}
		e.preventDefault();

	});

}

function isLogin(){
	var status = $("#log-btn").attr("status");
	console.log(status);
	if(status == "loggedin"){
		return true;
	}else{
		return false;
	}
}
