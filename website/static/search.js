var searchEnabled = false;

$(document).ready(function() {
    //Trigger Searchbar
    $('*').keypress(function() {
        if(searchEnabled == false) {
            searchEnabled = true;
            enableSearch();
        }
    });

    $('#inSearch').on('keyup', function(e) {
        if(e.keyCode === 13) {
            disableSearch();
            return;
        }
        var content = $(this).val().toLowerCase();
        if(content == '') {
            disableSearch();
            return;
        } else {

        }
        $('#levelTable tr').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(content) > -1);
        });
    });
});

function enableSearch() {
    $('#inSearch').removeClass('invisible');
    $('.invisible-item').removeClass('invisible');
    $('#inSearch').focus();
}

function disableSearch() {
    $('.invisible-item').addClass('invisible');
    $('.visible-item').css('display', '');
    $('#inSearch').addClass('invisible');
    $('#inSearch').val('');
    searchEnabled = false;
}
