$(document).ready( function() {

	deleteReviewAjax();

});

function deleteReviewAjax(){
	$(".delete-btn").click(function(e){
		e.preventDefault();
		var review_id = $(this).attr("review-id");
		var review_li = $("li[li-id*=" + review_id + "]");
		var delete_link = $(this).attr("href");
		$(".delete-popup").modal();
		$(".delete-confirm").click(function(){
			$.ajax({
			url: delete_link,
			success:function(){				
				$("li[li-id*=" + review_id + "]").remove();

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

	$(".delete-from-view-page").click(function(e){
		e.preventDefault();
		var delete_link = $(this).attr("href");
		$(".delete-popup").modal();
		$(".delete-confirm").click(function(){
			$.ajax({
			url: delete_link,
			success:function(){				
				document.write(html);
				document.close();
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