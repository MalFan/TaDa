$(document).ready( function() {	
	resetPasswordValidation();
	changePasswordValidation();
});

function resetPasswordValidation(){
	 $("#reset-password-form").find("input").each(function(){
		if($(this).next().hasClass("errorlist")){
			var error = $(this).next().find("li").html();
			$(this).next().remove()
			$(this).addClass("input_warning");
			$(this).attr("placeholder",error);
		}
	});
}

function changePasswordValidation(){
	$("#change-password-form").submit( function( e ) {
				
		e.preventDefault();

		var input_password0 = $(this).find('#id_old_password');
		var input_password1 = $(this).find('#id_new_password1');
		var input_password2 = $(this).find('#id_new_password2');
		content_password0 = input_password0.val();
		content_password1 = input_password1.val();
		content_password2 = input_password2.val();
		var isValid = true;
		if(!content_password0.trim()){
		  input_password0.attr("placeholder","Original password can't be empty.");
		  input_password0.attr("class","form-control input_warning");
		  isValid = false;
		}else{
		  input_password0.removeAttr("placeholder");
		  input_password0.attr("class","form-control");
		}

		if(!content_password1.trim()){
		  input_password1.attr("placeholder","Password can't be empty.");
		  input_password1.attr("class","form-control input_warning");
		  isValid = false;
		}else if(content_password0.trim() == content_password1.trim()){
		  input_password1.attr("placeholder","New password can't be same with old password.");
		  input_password1.attr("class","form-control input_warning");
		  input_password1.val("");
		  input_password2.val("");
		  isValid = false;
		}else{
		  input_password1.removeAttr("placeholder");
		  input_password1.attr("class","form-control");
		}

		if(!content_password2.trim()){
		  input_password2.attr("placeholder","Confirm password can't be empty.");
		  input_password2.attr("class","form-control input_warning");
		  isValid = false;
		}else if(content_password2.trim() != content_password1.trim()){
		  input_password2.attr("placeholder","Confirm password doesn't match.");
		  input_password2.attr("class","form-control input_warning");
		  input_password2.val("");
		  isValid = false;
		}else{
		  input_password2.removeAttr("placeholder");
		  input_password2.attr("class","form-control");
		}

		if(isValid){
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
					console.log(html);
					if(html == "error"){
						input_password0.val("");
		  				input_password0.attr("class","form-control input_warning");					    
		  				input_password0.attr("placeholder","Incorrect original password.");
					}		 
					else{
						document.write(html);
						document.close();
					}   
				},
				error: function() 
				{
					//if fails
					alert( "error" );      
				}
			});
		}


	});
}


