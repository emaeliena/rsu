$(document).ready(function() {
    $.ajax({
        url: 'https://rsuapi.herokuapp.com/v1/rates/USD'
    }).done(function(data) {
        $('table#rates tbody').empty();
        $('table#rates tbody').append('<tr class="dates"></tr>');
        $('table#rates tbody').append('<tr class="values"></tr>');
        $.each(data, function(index, value) {
            var date = new Date(value.date);
            $('table#rates tbody tr.dates').prepend('<th>' + date.toISOString().slice(0, 10) + '</th>');
            $('table#rates tbody tr.values').prepend('<td>' + value.value + '</td>');
        });
    });
});