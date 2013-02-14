
$(function() {

    /* Global Vars */

    var details  = $('.detail');
    var articles = $('.subprocess');
    var moreInfo = $('.more-info');


    /* Handlers */

    var detailHandler = function() {
    	var index = $(this).parent().index();
    	articles.addClass("hidden").eq(index).removeClass("hidden");
    }

    var externalResultsHandler = function() {
        var chevron = $(this).children();
        chevron.toggleClass('icon-chevron-down icon-chevron-up');

        var index = $(this).parent().index();

        var visibleArticle = articles.filter(function(i) {
            return !articles.eq(i).hasClass('hidden');
        })

        var rows = visibleArticle.find('.tasks').children();
        rows.eq(index + 1).fadeToggle();
    }


    /* Event Assignments */

    details.on('click', detailHandler);
    moreInfo.on('click', externalResultsHandler);

});
