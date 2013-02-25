
$(function() {

    /* Global Vars */

    var processes  = $('.process');
    var articles = $('.subprocess');
    var moreInfo = $('.more-info');

    var currentArticle;
    var pid = 0;
    var HIDDEN = 'hidden';


    /* Handlers */

    var processHandler = function() {
        var row = $(this);
        currentArticle = row.index();

        pid = parseInt( row.find('.pid').text() );

        toggleSelectedProcess( row );
    };


    var subprocessHandler = function() {
        var select = $(this);
        var selectedOption = select[0].selectedIndex;
        var tabs = select.siblings('.tab');
        tabs.addClass( HIDDEN );
        tabs.eq(selectedOption).removeClass( HIDDEN );
    };


    var externalResultsHandler = function() {
        var chevron = $(this).children();
        chevron.toggleClass('icon-chevron-down icon-chevron-up');

        var index = $(this).parent().index();

        var visibleArticle = articles.filter(function(i) {
            return !articles.eq(i).hasClass( HIDDEN );
        })

        var rows = visibleArticle.find('.tasks').children();
        rows.eq(index + 1).fadeToggle();
    };


    var refreshHandler = function() {
        window.location.href += ("?pid=" + pid);
    };


    var searchSelectedProcessHandler = function() {
        pid = parseInt( getParam('pid') );

        var selectedRow = processes.filter(function(i) {
            var column = processes.eq(i).find('.pid')
            var rowPID = parseInt( column.text() );
            return rowPID === pid;
        });

        currentArticle = proc.index();

        toggleSelectedProcess( selectedRow );
    };


    /* Auxiliary Functions */

    var toggleSelectedProcess = function(row) {
        var BLUE = 'blue';

        articles.addClass( HIDDEN );
        articles.eq( currentArticle ).removeClass( HIDDEN );

        processes.removeClass( BLUE );
        row.addClass( BLUE );
    };


    var getParam = function(param) {
        var params = window.location.search.slice(1);
        var i = params.indexOf('=');
        var p = params.substring(0, i);

        var res = "";

        // Loop to search every param

        if (p == param) {
            var last = params.indexOf('&');
            if (last === -1) {
                last = params.length;
            }

            res = params.substring(i+1, last);
        }

        return res;
    };

    /*
    var getURLParameter = function (sParam) {
        var sPageURL = window.location.search.slice(1);
        var sURLVariables = sPageURL.split('&');

        for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] == sParam) {
                return sParameterName[1];
            }
        }

        return "";
    }​;
    /


    /* Event Assignments */

    processes.on('click', processHandler);
    moreInfo.on('click', externalResultsHandler);

    $('#refresh').on('click', refreshHandler);
    $('.select').on('change', subprocessHandler);
    $('window').on('load', searchSelectedProcessHandler);


    /* Initialization */

    for (var i = 0; i < articles.length; i++) {
        var a = articles.eq(i);
        a.find('.tab').first().removeClass( HIDDEN );
    };

});
