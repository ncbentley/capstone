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
        $('.new-title').text("Edit Wireframe")
        $('#submit').val('Update Wireframe')
    })
    $('.delete').click(function(event) {
        let del = $(event.target.parentNode);
        if (del.data('action') == undefined) {
            del = $(event.target);
        }
        $('#delete-form').attr('action', del.data('action'))
    })
    $('.add-btn').click(function(event) {
        $('#form').attr('action', formAction)
        $('#form-data').html(formData)
        $('.new-title').text("Create New Wireframe")
        $('#submit').val('Create Wireframe')
    })
    $('.wireframe-image').click(function(event) {
        const wireframe = $(event.target).data('wireframe')
        window.location.href = `/image/${wireframe}/`
    })
})