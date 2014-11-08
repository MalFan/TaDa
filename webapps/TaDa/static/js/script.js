$(document).ready(function() {
    var away = false;

    $('.back-to-top-link').click(function() {
    	console.log("clicked");
        $("html, body").animate({scrollTop: 0}, 'slow');
    });
}); 

