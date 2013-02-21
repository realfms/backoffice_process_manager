
$(function() {

    /* Global Vars */

    var processes  = $('.process');
    var articles = $('.subprocess');
    var moreInfo = $('.more-info');

    var currentArticle;
    var HIDDEN = 'hidden';


    /* Handlers */

    var processHandler = function() {
        var TIME = 500;
        var BLUE = 'blue';

        var row  = $(this);
    	currentArticle = row.index();

        articles.addClass( HIDDEN );
        articles.eq( currentArticle ).removeClass( HIDDEN );

        processes.removeClass( BLUE );
        row.addClass( BLUE );
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


    /* Event Assignments */

    processes.on('click', processHandler);
    moreInfo.on('click', externalResultsHandler);
    $('.select').on('change', subprocessHandler);


    /* Initialization */

    for (var i = 0; i < articles.length; i++) {
        var a = articles.eq(i);
        a.find('.tab').first().removeClass( HIDDEN );
    };

});
