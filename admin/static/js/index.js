$document.ready(() => {
    $('input[name="net_connection"').change(() => {
        if($('#net_yes').is(':checked')) {
            $('#net_section').slideDown();

        } else {
            $('#net_section').slideUp();
        }
    });
});