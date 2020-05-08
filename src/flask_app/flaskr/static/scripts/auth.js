$("form").submit(function(e){
        e.preventDefault();
        alert('it is working!');
    });

$(document).ready(function(){
    $('sfsaf').click(function(){
        var password = $('#password').val();
        alert(password);
        var password2 = $('#password2').val();
        if(password != password2){
            alert('the passwords didn\'t match!');
        }

    });
});

$(document).ready(function(){
  $("h1").click(function(){
    $(this).hide();
  });
});
