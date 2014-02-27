$(document).ready(function() {
    $('#page').mapster({
                mapKey: 'data-id',
                fillColor: 'ff0000',
                fillOpacity: 0.3, 
    onMouseover: function (e) {
        $("#" + e.key).addClass("selected");
    },
    onMouseout: function (e) {
        $("#" + e.key).removeClass("selected");
    }
                
    }).mapster('resize', 500);

    $("span").mouseenter(function() {
        $('area[data-id='+$(this).attr("id")+']').mapster("highlight");
    });

    $("span").mouseout(function() {
        $('#page').mapster("highlight", false);
    });
});
