
$(document).ready(function() {
    $(".edit_course").on("click", function() {
        var id = $(this).prop("name").split("_")[1];
    });

    $(".remove_course").on("click", function(){
        var info = $(this).prop("name").split("_");
        
        if (confirm("Are you sure you want to remove the course '" + info[0] + "'?")) {
            $.post("/remove_course", {c_id: info[1]});
        }
    });
});