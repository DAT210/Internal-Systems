
/*
var ingredients = [
    "ingredient alpha",
    "ingredient bravo",
    "ingredient charlie",
    "ingredient delta",
    "ingredient echo",
    "ingredient fractal",
    "ingredient gamma",
    "ingredient hector",
    "ingredient indie",
    "ingredient jodie"
];
*/

var ingredients;
var allergenes;

var authLevel = 2;

$(document).ready(function() {
    var visible = [];
    init();
    
    function removeCourse() {
        if (authLevel > 1) {
            var info = $(this).prop("name").split("_");
            
            if (confirm("Are you sure you want to remove the course '" + info[0] + "'?")) {
                $.get("/remove_course", {c_id: info[1]}, function (data) {
                    $(".course_display").html(data);
                    init();
                });
            }
        } else {
            alert("PERMISSION DENIED");
        }
    }

    function removeIngredientFromCourse() {
        if (authLevel > 1) {
            var info = $(this).prop("name").split("_");
            
            if (confirm("Are you sure you want to remove this ingredient from the course?")) {
                $.get("/remove_ingredient_from_course", {c_id: info[0], i_id: info[1]}, function (data) {
                    $(".course_display").html(data);
                    init();
                });
            }
        } else {
            alert("PERMISSION DENIED");
        }
    }

    function addIngredientToCourse() {
        if (authLevel > 1) {
            var c_id = $(this).prop("id").split("-")[1];
            var i_id = $("#autocomplete_ingredient_" + c_id).prop("name");

            $.get("/add_ingredient_to_course", {c_id: c_id, i_id: i_id}, function (data) {
                $(".course_display").html(data);
                init();
            });

        } else {
            alert("PERMISSION DENIED");
        }
    }
    
    function init() {
        updateAutocomplete();

        $(".remove_course").on("click", removeCourse);
        $(".remove_ingredient_from_course").on("click", removeIngredientFromCourse);
        $(".add_ingredient").on("click", addIngredientToCourse)

        var ingredientInputs = $(".ingredient-input");
        for (var i = 0; i < ingredientInputs.length; i++) {
            var ingredientsIn = [];
            for (var j = 0; j < ingredients.length; j++) {
                ingredientsIn.push(ingredients[j].i_name);
            }
            autocomplete(ingredientInputs[i], ingredientsIn);
        }

        for (var i = 0; i < visible.length; i++) {
            if (visible[i]) {
                $(".hidden_admin_" + i).css("display", "inline-block");
            } else {
                $(".hidden_admin_" + i).css("display", "none");
            }
        }

        if (authLevel < 2) {
            $(".edit_course").css("display", "none");
        } else {
            initAdminFunctions();
        }
    }

    function updateAutocomplete() {
        // I don't know if there are any better solutions for these yet, but these requests
        // have to be synchronous as far as I know in order to work properly.

        // Update Ingredients
        $.ajax({
            url: "/get_ingredients",
            type: "get",
            async: false,
            success: function(data) {
                ingredients = JSON.parse(data);
            }
        });

        // Update Allergenes
        $.ajax({
            url: "/get_allergenes",
            type: "get",
            async: false,
            success: function(data) {
                allergenes = JSON.parse(data);
            }
        });
    }

    function initAdminFunctions() {
        if (authLevel < 2) {
            alert("ACCESS DENIED");
        } else {
            $(".edit_course").css("display", "inline-block");
            $(".edit_course").on("click", function() {
                var id = $(this).prop("name").split("_")[1];
                var idInt = parseInt(id);
                if (visible[idInt]) {
                    $(".hidden-admin-" + id).css("display", "none");
                    visible[idInt] = false;
                } else {
                    $(".hidden-admin-" + id).css("display", "inline-block");
                    visible[idInt] = true;
                }
            });
        }
    }
});

// GOTTEN FROM W3 SCHOOLS, BUT IT WORKS SO OKAY
function autocomplete(inp, arr) {
    var currentFocus;
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);
        for (i = 0; i < arr.length; i++) {
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                b = document.createElement("DIV");
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.innerHTML += "<input type='hidden' value='" + i + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    inp.name = parseInt(this.getElementsByTagName("input")[1].value) + 1;
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(x);
        } else if (e.keyCode == 38) { //up
            currentFocus--;
            addActive(x);
        } else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
    // END OF W3 SCHOOLS AUTOCOMPLETE
}