$(document).ready( function() {

	deleteReviewAjax();

});

function deleteReviewAjax(){
	$("[title='deleteReview']").click(function(){
		var review_id = $(this).attr("review-id");
		var review_li = $("li[li-id*=" + review_id + "]");
		$.ajax({
			url: $(this).attr("href"),
			success:function(){
				
				$("li[li-id*=" + review_id + "]").remove();
			},
			error:function(){
				
			}

		});
		
	});
}