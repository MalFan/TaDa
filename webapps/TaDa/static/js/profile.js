$(document).ready(function() {
    $('.btn-edit').click( function(){
        $('.profile-intro').toggle();
    });

     $('.btn-follow').click( function(){

        var status = $(this).text();
        if(status == 'follow'){
            $(this).text('unfollow');
        }else{
            $(this).text('follow');
        }
     });

     $('.user-profile-photo').mouseover(function(){
        $('.btn-change').slideDown();
     });

     $('#photo-preview').hide();


    $(".choose-photo").change(function(){
        readURL(this);
        $('#photo-preview').show();
    });

}); 

 function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function (e) {
            $('#photo-preview').attr('src', e.target.result);
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}
  
