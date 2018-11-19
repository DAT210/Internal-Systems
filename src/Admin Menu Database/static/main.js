$(document).ready(function() {
    init();

    function init() {
        initTabSwap();
    }

    function initTabSwap() {
        $(".tab-swap").on("click", function () {
            var link = $(this).prop("name");
            $(".db_tab").css("display", "none");
            $("." + link + "_display").css("display", "block");
        });
    }
});