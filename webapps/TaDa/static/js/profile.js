$(document).ready(function() {
    $('.btn-edit').click( function(){
        $('.profile-intro').toggle();
    });

     $(".btn-follow").click(function(e){
        if(isLogin()){
            console.log("1");
            var btnHref = $(".btn-follow").attr( "href" );
            $.ajax(
            {
                url: btnHref,
                success:function(response) 
                {
                    $(".btn-follow").html(response);
                        
                },
                error: function() 
                {    
                }
            });         
        }else{
            $('.login-popup').modal();
        }
        e.preventDefault(); //STOP default action
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
  
function isLogin(){
    var status = $("#log-btn").attr("status");
    if(status == "loggedin"){
        return true;
    }else{
        return false;
    }
}