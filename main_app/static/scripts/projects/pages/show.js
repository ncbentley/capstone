$(function() {
    const formData = $('#form-data').html()
    const formAction = $('#form').attr('action')
    $('.edit').click(function(event) {
        let edit = $(event.target.parentNode);
        if (edit.data('form') == undefined) {
            edit = $(event.target);
        }
        const form = edit.data('form')
        const action = edit.data('action')
        $('#form').attr('action', action)
        $('#form-data').html(form)
        $('#submit').val('Update Wireframe')
    })
    $('.add-btn').click(function(event) {
        console.log(event)
        $('#form').attr('action', formAction)
        $('#form-data').html(formData)
        $('#submit').val('Create Wireframe')
    })
    $('.wireframe-image').click(function(event) {
        const wireframe = $(event.target).data('wireframe')
        window.location.href = `/image/${wireframe}/`
    })
})