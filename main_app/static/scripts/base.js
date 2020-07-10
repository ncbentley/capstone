$(function() {
    $('#login-btn').click(function() {
        $('#login-tab')[0].click();
    })
    $('#register-btn').click(function() {
        $('#register-tab')[0].click();
    })

    $('#profile-submit').click(function(event) {
        event.preventDefault();
        $('#origin').val(window.location.href)
        $('#profile-form')[0].submit();
    })
})

