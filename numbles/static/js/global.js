/**
 * Copyright 2017 - Nathan Osman
 */

(function() {

    // On page load, find and bind all of the toggles
    $(function() {
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
