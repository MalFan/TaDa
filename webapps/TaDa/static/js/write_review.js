$(document).ready( function() {

	writeReviewAjax();

});

function writeReviewAjax() {
	$("#review-form").submit( function( e ) {
		
		var input_title = $("#id_title")
		var input_text = $("#id_text")
		var content_title = input_title.val();
		var content_text = input_text.val();
		var isValid = true;
		if (!content_title.trim()) {
        // is empty or whitespace
		  input_title.attr("placeholder","Cannot post an empty title.");
		  input_title.attr("class","form-control input_warning");
		  isValid = false;
		}else{
			input_title.removeAttr("placeholder");
			input_title.attr("class","form-control");
		}
		if(!content_text.trim()){
		  input_text.attr("placeholder","Cannot post an empty review.");
		  input_text.attr("class","form-control input_warning");
		  isValid = false;
		}else{
		  input_text.removeAttr("placeholder");
		  input_text.attr("class","form-control");
		}
		if(!isValid){

			e.preventDefault();

		}
	});

}


