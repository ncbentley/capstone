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
})