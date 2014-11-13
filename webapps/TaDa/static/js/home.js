$(function() {
	$('.coverflow').coverflow();	
});

$('.upcoming-group-wrapper').on('click', function() {
    $(this).find('.upcoming-movie-wrapper').slideToggle();
    $('html, body').animate({
    scrollTop: $(this).offset().top
}, 1000);  
});
