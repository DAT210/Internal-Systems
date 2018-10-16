

var ingredients;
var allergenes;

var authLevel = 2;

$(document).ready(function() {
    var inEdit = [];
    init();

    
    function init() {
        updateAutocomplete();
        
        // EDIT COURSE INFORMATION
        $("#add_course").on("click", addCourse);
        $(".remove_course").on("click", removeCourse);
        
        $(".add_ingredient_to_course").on("click", addIngredientToCourse);
        $(".remove_ingredient_from_course").on("click", removeIngredientFromCourse);
        
        $(".edit_course_name").on("click", editCourseName);
        $(".edit_course_price").on("click", editCoursePrice);
        $(".edit_course_category").on("click", editCourseCategory);
        $(".edit_course_description").on("click", editCourseDescription);
        
        // EDIT INGREDIENT INFORMATION
        $("#add_ingredient").on("click", addIngredient);
        $(".remove_ingredient").on("click", removeIngredient);
        
        $(".add_allergene_to_ingredient").on("click", addAllergeneToIngredient);
        $(".remove_allergene_from_ingrdient").on("click", removeAllergeneFromIngredient);

        // EDIT ALLERGENE INFORMATION
        $("#add_allergene").on("click", addAllergene);
        $(".remove_allergene").on("click", removeAllergene);

        var ingredientInputs = $(".ingredient-input");
        for (var i = 0; i < ingredientInputs.length; i++) {
            var ingredientsIn = [];
            for (var j = 0; j < ingredients.length; j++) {
                ingredientsIn.push(ingredients[j].i_name);
            }
            autocomplete(ingredientInputs[i], ingredientsIn);
        }
    
        for (var i = 0; i < inEdit.length; i++) {
            if (inEdit[i]) {
                $(".hidden-default-" + i).css("display", "inline-block");
                $(".hidden-edit-" + i).css("display", "none");
            } else {
                $(".hidden-default-" + i).css("display", "none");
                $(".hidden-edit-" + i).css("display", "inline-block");
            }
        }
        initAdminFunctions();
    }

    function addCourse() {
        $.get("/add_course", function (data) {
            $(".course_display").html(data);
            init();
        });
    }

    function removeCourse() {
        var info = $(this).prop("name").split("_");
        
        if (confirm("Are you sure you want to remove the course '" + info[0] + "'?")) {
            $.get("/remove_course", {c_id: info[1]}, function (data) {
                $(".course_display").html(data);
                init();
            });
        }
    }

    function removeIngredientFromCourse() {
        var info = $(this).prop("name").split("_");
        
        if (confirm("Are you sure you want to remove this ingredient from the course?")) {
            $.get("/remove_ingredient_from_course", {c_id: info[0], i_id: info[1]}, function (data) {
                $(".course_display").html(data);
                init();
            });
        }
    }

    function addIngredientToCourse() {
        var c_id = $(this).prop("id").split("-")[1];
        var i_id = $("#autocomplete_ingredient-" + c_id).prop("name");

        $.get("/add_ingredient_to_course", {c_id: c_id, i_id: i_id}, function (data) {
            $(".course_display").html(data);
            init();
        });
    }

    function addIngredient() {
        $.get("/add_ingredient", function (data) {
            $(".ingredient_display").html(data);
            init();
        });
    }
    
    function removeIngredient() {
        var info = $(this).prop("name".split("_"));
    
        if (confirm("Are you sure you want to remove the ingredient '" + info[0] + "'?")) {
            $.get("/remove_ingredient", {i_id: info[1]}, function (data) {
                $(".ingredient_display").html(data);
                init();
            });
        }
    }

    function addAllergeneToIngredient() {
        var i_id = $(this).prop("id").split("-")[1];
        var a_id = $("#autocomplete_allergene-" + i_id).prop("name");

        $.get("/add_allergene_to_course", {i_id: i_id, a_id: a_id}, function (data) {
            $(".ingredient_display").html(data);
            init();
        });
    }

    function removeAllergeneFromIngredient() {
        var info = $(this).prop("name").split("_");
        
        if (confirm("Are you sure you want to remove this allergene from the ingredient?")) {
            $.get("/remove_ingredient_from_course", {i_id: info[0], a_id: info[1]}, function (data) {
                $(".ingredient_display").html(data);
                init();
            });
        }
    }

    function addAllergene() {
        $.get("/add_allergene", function (data) {
            $(".allergene_display").html(data);
            init();
        });
    }
    
    function removeAllergene() {
        var info = $(this).prop("name".split("_"));
    
        if (confirm("Are you sure you want to remove the allergene '" + info[0] + "'?")) {
            $.get("/remove_allergene", {a_id: info[1]}, function (data) {
                $(".allergene_display").html(data);
                init();
            });
        }
    }

    function editCourseName() {
        var c_id = $(this).prop("name");
        var c_name = $("#course-edit-name_" + c_id).val();
        $.get("/edit_course_name", {c_id: c_id, c_name: c_name}, function (data) {
            $(".course_display").html(data);
            init();
        });
    }

    function editCoursePrice() {
        var c_id = $(this).prop("name");
        var price = $("#course-edit-price_" + c_id).val();
        $.get("/edit_course_price", {c_id: c_id, price: price}, function (data) {
            $(".course_display").html(data);
            init();
        });
    }

    function editCourseCategory() {
        var c_id = $(this).prop("name");
        var category = $("#course-edit-category_" + c_id).val();
        $.get("/edit_course_category", {c_id: c_id, category: category}, function (data) {
            $(".course_display").html(data);
            init();
        });
    }

    function editCourseDescription() {
        var c_id = $(this).prop("name");
        var description = $("#course-edit-description_" + c_id).val();
        $.get("/edit_course_description", {c_id: c_id, description: description}, function (data) {
            $(".course_display").html(data);
            init();
        });
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
        $(".edit_course").css("display", "inline-block");
        $(".edit_course").on("click", function() {
            var id = $(this).prop("name").split("_")[1];
            var idInt = parseInt(id);
            if (inEdit[idInt]) {
                $(".hidden-default-" + id).css("display", "none");
                $(".hidden-edit-" + id).css("display", "inline-block");
                inEdit[idInt] = false;
            } else {
                $(".hidden-default-" + id).css("display", "inline-block");
                $(".hidden-edit-" + id).css("display", "none");
                inEdit[idInt] = true;
            }
        });
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