$(document).ready( function() {

	deleteCommentAjax();

});

function deleteCommentAjax(){
	$("[title='deleteComment']").click(function(){
		var comment_id = $(this).attr("comment-id");
		var comment_li = $("li[li-id*=" + comment_id + "]");
		$.ajax({
			url: $(this).attr("href"),
			success:function(){
				$("li[li-id*=" + comment_id + "]").remove();
			},
			error:function(){

			}

		});
		
	});
}