$(document).ready(function(){
    $("#error_box").hide();
});

$(document).ready(function(){
    $("form").submit(function(e){
        var password = $('#password').val();
        var password2 = $('#password2').val();

        if(password.length < 8){
            e.preventDefault();
            $("#error_box").html("Password has to be longer than 7 characters");
        }

        if(password != password2){
            e.preventDefault();
            $("#error_box").html("Passwords have to match");
        }

        $("#error_box").show();

  });
});
