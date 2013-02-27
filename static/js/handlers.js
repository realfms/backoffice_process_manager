
$(function() {

    /* Global Vars */

    var processes  = $('.process');
    var articles = $('.subprocess');
    var moreInfo = $('.more-info');

    var currentArticle = 0;
    var pid = 0;
    var HIDDEN = 'hidden';


    /* Handlers */

    var processHandler = function(event) {
        event.preventDefault();
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
        /*
        var url = window.location.href;
        var i = url.lastIndexOf('pid');

        if ( i == -1 ) {
            window.location.href += ("?pid=" + pid);

        } else {
            var base = url.substring(0, i);
            base += ("pid=" + pid);
            window.location.href = base;
        }
        */
        window.location.reload();
    };


    var searchSelectedProcessHandler = function() {
        pid = parseInt( getParam('pid') );

        /*
        var selectedRow = processes.filter(function(i) {
            var column = processes.eq(i).find('.pid')
            var rowPID = parseInt( column.text() );
            return rowPID === pid;
        });
        */

        for (var i = 0; i < processes.length; i++) {
            var row = processes.eq(i);
            var rowPID = parseInt( row.find('.pid').text() );

            if ( rowPID === pid ) {
                currentArticle = row.index();
                toggleSelectedProcess( row );
            }
        }

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
        var url   = window.location.href;
        var index = url.lastIndexOf('?') + 1;
        var end   = index + param.length;
        var p     = url.substring(index, end);

        var res = "";
        if (p == param) {
            res = url.substring(end + 1, url.length);
        }

        return res;
    };


    /* Event Assignments */

    processes.on('click', processHandler);
    moreInfo.on('click', externalResultsHandler);

    $('#refresh').on('click', refreshHandler);
    $('.select').on('change', subprocessHandler);
    $(document).on('ready', function(){
        //searchSelectedProcessHandler();

        /* Initialization */

        for (var i = 0; i < articles.length; i++) {
            var a = articles.eq(i);
            a.find('.tab').first().removeClass( HIDDEN );
        }

        toggleSelectedProcess( processes.first() );
    });



});
