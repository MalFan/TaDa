$(document).ready( function() {
	$("#reset-password-form").submit( function( e ) {
				
		// e.preventDefault();
		
		var input_password1 = $(this).find('#id_password1');
		var input_password2 = $(this).find('#id_password2');
		content_password1 = input_password1.val();
		content_password2 = input_password2.val();
		var isValid = true;
		if(!content_password1.trim()){
		  input_password1.attr("placeholder","Password can't be empty.");
		  input_password1.attr("class","form-control input_warning");
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

		if(!isValid){
			e.preventDefault();
		}


	});

	$("#change-password-form").submit( function( e ) {
				
		// e.preventDefault();

		var input_password0 = $(this).find('#id_password0');
		var input_password1 = $(this).find('#id_password1');
		var input_password2 = $(this).find('#id_password2');
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

		if(!isValid){
			e.preventDefault();
		}


	});
});


