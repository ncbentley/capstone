$(function() {
    $('.sprint:not(.disabled), .page').click(function(event) {
        node = event.target;
        while (!$(node).is('.sprint') && !$(node).is('.page')) {
            node = node.parentNode;
        }
        window.location.href = $(node).data('url');
    })
    $('.sprint.completed input[type="checkbox"]').prop("checked", true);
    $($('.sprint:not(.completed)')[$('.sprint:not(.completed)').length - 1]).nextAll().addClass('disabled');
})