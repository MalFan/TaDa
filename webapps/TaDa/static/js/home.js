$(function() {
	$('.coverflow').coverflow();
	$('.coverflow-wrapper').removeClass("invisible");
});

$('.upcoming-date-wrapper').on('click', function() {
    $(this).next().slideToggle();
//     $('html, body').animate({
//     scrollTop: $(this).offset().top
// }, 1000);  
});
