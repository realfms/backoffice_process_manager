
$(function() {

    /* Global Vars */

    var details  = $('.process');
    var articles = $('.subprocess');
    var moreInfo = $('.more-info');
    var currentArticle;

    /* Handlers */

    var detailHandler = function() {
        var TIME = 500;
    	currentArticle = $(this).index();
        articles.addClass('hidden')
        articles.eq( currentArticle ).removeClass('hidden')
/*
    	articles.animate({
            "margin-left" : "-5000px",
            "opacity"     : "0"
        }, TIME);

        articles.eq( currentArticle ).animate({
            "margin-left" : "0px",
            "opacity"     : "1"
        }, TIME);
*/
    };


    var subprocessSelectionHandler = function() {
        var select = $(this);
        var selectedOption = select[0].selectedIndex;
        var tabs = select.siblings('.tab');
        tabs.addClass('hidden');
        tabs.eq(selectedOption).removeClass('hidden');
    };


    var externalResultsHandler = function() {
        var chevron = $(this).children();
        chevron.toggleClass('icon-chevron-down icon-chevron-up');

        var index = $(this).parent().index();

        var visibleArticle = articles.filter(function(i) {
            return !articles.eq(i).hasClass('hidden');
        })

        var rows = visibleArticle.find('.tasks').children();
        rows.eq(index + 1).fadeToggle();
    };


    /* Event Assignments */

    details.on('click', detailHandler);
    moreInfo.on('click', externalResultsHandler);

    $('.select').on('change', subprocessSelectionHandler);

    for (var i = 0; i < articles.length; i++) {
        var a = articles.eq(i);
        a.find('.tab').first().removeClass('hidden');
    };

});
