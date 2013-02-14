
$(function() {

var details = $(".detail");
var articles = $(".subprocess");

function detailHandler(e) {
	var index = $(this).parent.index();
	articles.addClass("hidden");
	articles.eq(index).removeClass("hidden");
}

details.on('click', detailHandler);

});