$(document).ready(function() {

    var queryRates = function(date) {
        var url = 'http://127.0.0.1:5000/v1/rates/USD';
        if (date != '') {
            url += '?date=' + date;
        }
        $.ajax({
            url: url
        }).done(function(data) {
            var lastDate = new Date(data[0].date).toISOString().slice(0, 10);
            var $searchDateWidget = $('#search_date');
            if ($searchDateWidget.val() == '') {
                $searchDateWidget.val(lastDate);
            }
            $('table#rates tbody').empty();
            $('table#rates tbody').append('<tr class="dates"></tr>');
            $('table#rates tbody').append('<tr class="values"></tr>');
            $.each(data, function(index, value) {
                var date = new Date(value.date);
                $('table#rates tbody tr.dates').prepend('<th>' + date.toISOString().slice(0, 10) + '</th>');
                $('table#rates tbody tr.values').prepend('<td>' + value.value + '</td>');
            });
        });
    };

    $('#search_date').change(function(event) {
        queryRates(event.target.value);
    });

    $('#search_date').datepicker({
        dateFormat: 'yy-mm-dd'
    });

    queryRates('');
});