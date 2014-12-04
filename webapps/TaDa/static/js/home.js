$(function() {
	$('.coverflow').coverflow();
	$('.coverflow-wrapper').removeClass("invisible");
});

$('.upcoming-date-wrapper').on('click', function() {
    $(this).next().slideToggle();
});
