$(document).ready( function() {

	deleteCommentAjax();

});

function deleteCommentAjax(){
	$(".delete-comment").click(function(e){
		e.preventDefault();
		var comment_id = $(this).attr("comment-id");
		var comment_li = $("li[li-id*=" + comment_id + "]");
		var delete_link = $(this).attr("href");
		$(".delete-popup").modal();
		$(".delete-confirm").click(function(){
			$.ajax({
				url: delete_link,
				success:function(){
					$("li[li-id*=" + comment_id + "]").remove();
					$(".delete-popup").modal('hide');
				},
				error:function(){

				}

			});
		});
		$(".delete-cancel").click(function(){
			$(".delete-popup").modal('hide');
		});
		
		
	});
}