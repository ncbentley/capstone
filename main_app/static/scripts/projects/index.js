$(function() {
    $('.project').click(function(event) {
        node = event.target;
        while (!$(node).is('.project')) {
            node = node.parentNode;
        }
        window.location.href = $(node).data('url')
    })
})