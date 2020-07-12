$(function() {
    $('input[type=checkbox]').click(function(event) {
        const id = $(event.target).attr('id').split('checkbox')[1];
        $.ajax({
            url: `/togglecomplete/${id}`
        });
    })
    $('.edit').click(function(event) {
        let node = event.target;
        while (!$(node).is('a')) {
            node = node.parentNode;
        }
        node = $(node.parentNode);
        node.addClass('hidden');
        $(node[0].previousElementSibling).removeClass('hidden');
    });
    $('.cancel').click(function(event) {
        event.preventDefault();
        node = $(event.target.parentNode.parentNode);
        node.addClass('hidden');
        $(node[0].nextElementSibling).removeClass('hidden');
    });
    $('.delete').click(function(event) {
        let node = event.target;
        while (!$(node).is('a')) {
            node = node.parentNode;
        }
        $('#delete-form').attr('action', $(node).data('url'))
    });

})