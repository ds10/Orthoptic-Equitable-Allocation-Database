var tableOffset = $("#institution-list").offset().top;
var $header = $("#institution-list > thead").clone();
var $fixedHeader = $("#header-fixed").append($header);

$(window).bind("scroll", function() {
    var offset = $(this).scrollTop();

    if (offset >= tableOffset && $fixedHeader.is(":hidden")) {
        $fixedHeader.show();
    }
    else if (offset < tableOffset) {
        $fixedHeader.hide();
    }
});