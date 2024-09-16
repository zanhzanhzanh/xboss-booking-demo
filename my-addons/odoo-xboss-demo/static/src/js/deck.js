odoo.define('odoo-xboss-demo.deck', function(require) {
    "use strict";
    $(document).ready(function () {
        // Function get Params
        var getUrlParameter = function getUrlParameter(sParam) {
            var sPageURL = window.location.search.substring(1),
                sURLVariables = sPageURL.split('&'),
                sParameterName,
                i;

            for (i = 0; i < sURLVariables.length; i++) {
                sParameterName = sURLVariables[i].split('=');

                if (sParameterName[0] === sParam) {
                    return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
                }
            }
            return false;
        };

        // Test
        // $(function () {
        //     setInterval(function () {
        //         console.log("Hello, world!");
        //     }, 1000);
        // });

        // Deck Function
        $('#deck-btn').on('click', function (e) {
            e.preventDefault();
            window.location.href = '/desk-form' + window.location.search;
        });

        // Deck Form Function
        $('#deck-form-btn').on('click', function (e) {
            e.preventDefault();

            $('.needs-validation').each(function () {
                if (this.checkValidity()) {
                    let data = {
                        'name': $('#name').val(),
                        'email': $('#email').val(),
                        'phone': $('#phone').val(),
                        'company': $('#company').val(),
                        'host': parseInt($('#meeting').val()),
                    }

                    // Save Data
                    sessionStorage.setItem('userData', JSON.stringify(data));

                    window.location.href = '/desk-ask' + window.location.search;
                }
                $(this).addClass('was-validated');
            });
        });

        // Deck Ask Function
        $('#submit-drinks').on('click', function() {
            let userData = JSON.parse(sessionStorage.getItem('userData'));
            let selectedDrinks = [];

            // Get All Selected
            $('input[name="drinks"]:checked').each(function () {
                selectedDrinks.push(parseInt($(this).val()));
            });

            userData['drinks_id'] = selectedDrinks;

            // Get Param station_id
            userData['station_id'] = parseInt(getUrlParameter('station_id')[1]);

            console.log(selectedDrinks);
            console.log(userData);

            let metaData = {
                'params': userData
            }

            // POST Request
            $.ajax({
                url: 'http://localhost:8888/visitor/create',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(metaData),
                success: function(response) {
                    // console.log('Data saved successfully:', response);
                    window.location.href = '/desk-success' + window.location.search;
                }
            });
        });

        // Deck Success Function
        $('#success-btn').on('click', function (e) {
            e.preventDefault();

            // Delete Data
            sessionStorage.removeItem('userData');

            window.location.href = '/desk' + window.location.search;
        });

        // Redirect for Deck Success Function
        if (window.location.href.indexOf("/desk-success") !== -1) {
            setTimeout(function() {
                // Delete Data
                sessionStorage.removeItem('userData');

                window.location.href = '/desk' + window.location.search;
            }, 5000);
        }
    });

    // Showing notification
    // var bus = require('bus.bus').bus;
    // var core = require('web.core');
    // var _t = core._t;
    // bus.on('visitor_channel', this, function (notifications) {
    //     notifications.forEach(function (notification) {
    //         var channel = notification[0];
    //         var message = notification[1];
    //         console.log('Hello')
    //
    //
    //         if (channel === 'visitor_channel') {
    //             console.log('Hello')
    //             alert(_t("New customer created: ") + message.name);
    //         }
    //     });
    // });
});
