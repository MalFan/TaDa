$(document).ready( function() {
	$("#login-form").submit( function( e ) {
				
		e.preventDefault();
		$(this).find("#login-error").remove();

		var input_username = $(this).find('#id_username');
		var input_password = $(this).find('#id_password');
		content_username = input_username.val();
		content_password = input_password.val();
		var isValid = true;
		if (!content_username.trim()) {
        // is empty or whitespace
		  input_username.attr("placeholder","Username can't be empty.");
		  input_username.attr("class","form-control input_warning");
		  isValid = false;
		}else{
			input_username.removeAttr("placeholder");
			input_username.attr("class","form-control");
		}
		if(!content_password.trim()){
		  input_password.attr("placeholder","Password can't be empty.");
		  input_password.attr("class","form-control input_warning");
		  isValid = false;
		}else{
		  input_password.removeAttr("placeholder");
		  input_password.attr("class","form-control");
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

					if(html == "error"){
		  				input_username.attr("class","form-control input_warning");
					    input_password.attr("class","form-control input_warning");
						$("#login-form").prepend("<p id = 'login-error'>Username and password don't match.</p>")
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

	$("#register-form").submit( function( e ) {
				
		e.preventDefault();
		$(this).find("p[id = 'register-error']").remove();

		var input_email = $(this).find('#id_email');
		var input_username = $(this).find('#id_username');
		var input_password1 = $(this).find('#id_password1');		
		var input_password2 = $(this).find('#id_password2');
		content_email = input_email.val();
		content_username = input_username.val();
		content_password1 = input_password1.val();
		content_password2 = input_password2.val();

		var isValid = true;
		if (!content_email.trim()) {
        // is empty or whitespace
		  input_email.attr("placeholder","Email can't be empty.");
		  input_email.attr("class","form-control input_warning");
		  isValid = false;
		}else{
			input_email.removeAttr("placeholder");
			input_email.attr("class","form-control");
		}
		if (!content_username.trim()) {
        // is empty or whitespace
		  input_username.attr("placeholder","Username can't be empty.");
		  input_username.attr("class","form-control input_warning");
		  isValid = false;
		}else{
			input_username.removeAttr("placeholder");
			input_username.attr("class","form-control");
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
					if(html == "username"){
		  				input_username.attr("class","form-control input_warning");						
						$("#register-form").prepend("<p id = 'register-error'>Username has already been taken.</p>")
					}
					else if(html == "email"){
						input_email.attr("class","form-control input_warning");						
						$("#register-form").prepend("<p id = 'register-error'>Email format isn't correct.</p>")
					
					}
					else if(html == "usernameemail"){
						input_username.attr("class","form-control input_warning");						
						$("#register-form").prepend("<p id = 'register-error'>Username has already been taken.</p>")
						input_email.attr("class","form-control input_warning");						
						$("#register-form").prepend("<p id = 'register-error'>Email format isn't correct.</p>")
										
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

	$("#email-form").submit( function( e ) {
				
		e.preventDefault();
		$(this).find("#email-error").remove();

		var input_email = $(this).find('#id_email');
		content_email = input_email.val();
		var isValid = true;
		if (!content_email.trim()) {
        // is empty or whitespace
		  input_email.attr("placeholder","Email can't be empty.");
		  input_email.attr("class","form-control input_warning");
		  isValid = false;
		}else{
			input_email.removeAttr("placeholder");
			input_email.attr("class","form-control");
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

					if(html == "failed"){
		  				input_email.attr("class","form-control input_warning");
						$("#email-form").prepend("<p id = 'email-error'>Email doesn't exist.</p>")
					}		 
					else{
						$("#email-modal").modal('hide');
						$("#email-confirm-modal").modal();
						$(".confirm-email").html("An email has been sent to "+content_email.trim()+", please click the link in the email to reset your password.");
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

});


