$(function() {
    $('.sprint, .page').click(function(event) {
        node = event.target;
        while (!$(node).is('.sprint') && !$(node).is('.page')) {
            node = node.parentNode;
        }
        if (!$(node).is('.disabled')) window.location.href = $(node).data('url');
    })
    $('.sprint.completed input[type="checkbox"]').prop("checked", true);
    if (userType === 'dev') $($('.sprint:not(.completed)')[0]).nextAll().addClass('disabled');
    $('#copy').click(function(event) {
        input = $('#url')[0];
        $(input).attr('disabled', false)
        input.select();
        input.setSelectionRange(0, 99999);
        document.execCommand("copy");
        $(input).attr('disabled', true)
        UIkit.notification({
            message: 'URL Copied. Share with client to connect project!',
            pos: 'top-center',
            status: 'success',
            timeout: 5000,
        })
    })
})