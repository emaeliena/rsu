$(document).ready(function() {

    var $searchDateWidget = $('#search_date');

    var queryRates = function(date) {
        var url = 'https://rsuapi.herokuapp.com/v1/rates/USD';
        if (date != '') {
            url += '?date=' + date;
        }
        $.ajax({
            url: url
        }).done(function(data) {
            var lastDate = new Date(data[0].date).toISOString().slice(0, 10);

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

    $searchDateWidget.change(function(event) {
        queryRates(event.target.value);
    });

    $searchDateWidget.datepicker({
        dateFormat: 'yy-mm-dd'
    });

    $('#nav_buttons button').click(function(event) {
        var direction = $(event.target).data('direction');
        var searchDate = new Date($searchDateWidget.val());
        if (direction == 'right') {
            searchDate.setDate(searchDate.getDate() + 5);
        } else {
            searchDate.setDate(searchDate.getDate() - 5);
        }
        $searchDateWidget.datepicker('setDate', searchDate);
        $searchDateWidget.change();
    });

    queryRates('');
});
