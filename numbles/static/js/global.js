/**
 * Copyright 2017 - Nathan Osman
 */

(function() {
    $(function() {

        // Initialize the select2 fields
        $("select").select2({
            theme: "bootstrap"
        });

        // Ensure select2 elements are cleared on form reset
        $('button[type=reset').click(function() {
            $("select", $(this).closest('form')).val(null).trigger('change');
        });

        // Bind all of the toggles
        $('.toggle').each(function() {
            var $this = $(this),
                id = $this.data('id');
            $this.click(function() {
                $.post(TOGGLE_URL, {
                    transaction: id
                }, function(d) {
                    if ('error' in d) {
                        alert("Error: " + d.error);
                    } else {
                        $this.removeClass().addClass('toggle fa ' +
                            (d.reconciled ?
                                'fa-check text-success' :
                                'fa-times text-danger'));
                    }
                });
                $this.removeClass().addClass('fa fa-spinner fa-spin');
            });
        });
    });
})();
