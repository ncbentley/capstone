$(function() {
    $('#sign-in').click(function(event) {
        event.preventDefault();
        console.log(event);
        $('#register-btn')[0].click();
    })
})