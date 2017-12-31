function initPopovers() {
    $('.popover-markup > .trigger').popover({
        html: true,
        title: function() {
            return $(this).parent().find('.head').html();
        },
        content: function() {
            return $(this).parent().find('.content').html();
        },
        container: 'body',
        placement: 'right',
    });
    $('.popover-markup > .trigger').click(function (e) {
        e.stopPropagation();
    });
    $(document).click(function (e) {
        if (($('.popover').has(e.target).length == 0) || $(e.target).is('.close')) {
            $('.popover-markup > .trigger').popover('hide');
        }
    });
}
