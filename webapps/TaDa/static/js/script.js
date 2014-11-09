$(document).ready(function() {
    var backtotop = $('.back-to-top-link');
    backtotop.click(function() {
    	console.log("clicked");
        $("html, body").animate({scrollTop: 0}, 'slow');
    });

    if ($(this).scrollTop() > 10) {
        backtotop.fadeIn();
    // otherwise fadeout button
    } else {
        backtotop.fadeOut();
    }
}); 

