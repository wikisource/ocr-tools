$(document).ready(function() {
    $('#page').mapster({
        mapKey: 'data-id',
        fillColor: 'ff0000',
        fillOpacity: 0.3,
        onMouseover: function (e) {
            $("#" + "orig-" + e.key).addClass("selected");
            $("#" + "corr-" + e.key).addClass("selected");
        },
        onMouseout: function (e) {
            $("#" + "orig-" + e.key).removeClass("selected");
            $("#" + "corr-" + e.key).removeClass("selected");
        }

    }).mapster('resize', 500);

    $("span").mouseenter(function() {
        $('area[data-id='+$(this).attr("id").replace(/\D+/,"")+']').mapster("highlight");
    });

    $("span").mouseout(function() {
        $('#page').mapster("highlight", false);
    });
});
