$(document).ready(function () {
    // https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
    // https://github.com/js-cookie/js-cookie/
    $('#user-create-form').on('submit', function (event) {
        event.preventDefault();
        event.stopPropagation();


        var data = new FormData();

        // https://api.jquery.com/jQuery/#jQuery-selector-context
        var $form = $(this);
        data.append('name', $('#name-input', $form).val());

        // https://api.jquery.com/jQuery.ajax/
        // https://www.mattlunn.me.uk/blog/2012/05/sending-formdata-with-jquery-ajax/
        // https://api.jquery.com/data/
        $.ajax({
            type: "POST",
            url: $('#name-input', $form).attr('data-ajax-check-url'),
            processData: false,
            contentType: false,
            data: data,
            dataType: 'json',
        }).done(function (data, textStatus, jqXHR) {
            console.log(data);
            console.log(textStatus);
            //alert("success");

            if (data.is_existed) {
                $('#name-input-msg', $form)
                    .text('用户名无效: 已经存在')
                    .addClass('error').removeClass('success')
            } else {
                $('#name-input-msg', $form)
                    .text('用户名有效')
                    .addClass('success').removeClass('error')
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
            console.log(textStatus);
            //alert("error");
        }).always(function () {
            //alert("complete");
        });
        ;
    });

});




