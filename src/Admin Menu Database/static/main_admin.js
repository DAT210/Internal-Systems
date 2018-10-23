
// Sindre Hvidsten
 
/********************************\
| GLOBAL VARIABLE INITIALIZATION | 
\********************************/
var ingredients = [];
var allergenes = [];
var categories = [];
var selections = [];
var selectionCategories = [];

var inEdit = {
    course: {editName: ".edit_course", isEdit: []},
    ingredient: {editName: ".edit_ingredient", isEdit: []},
    allergene: {editName: ".edit_allergene", isEdit: []},
    category: {editName: ".edit_category", isEdit: []},
    selection: {editName: ".edit_selection", isEdit: []},
    selectionCategory: {editName: ".edit_selection_category", isEdit: []}
}

var darkMode = false;

$(document).ready(function() {
    init();

    /**************************\
    | INITIALIZATION FUNCTIONS | 
    \**************************/
    function init() {
        initAutocompletion();
        initFunctionality();
        initModeSwitch();
    }
    
    function initFunctionality() {
        initCourses();
        initIngredients();
        initAllergenes();
        initCategories();
        initSelections();
        initSelectionCategories();
        initAdminFunctions();
    }

    function initAutocompletion() {
        updateIngredients();
        updateAllergenes();
        updateCategories();
        updateSelections();
        updateSelectionCategories();
    }

    function initAdminFunctions() {
        $("#add_course").on("click", addCourse);
        $("#add_ingredient").on("click", addIngredient);
        $("#add_allergene").on("click", addAllergene);
        $("#add_category").on("click", addCategory);
        $("#add_selection").on("click", addSelection);
        $("#add_selection_category").on("click", addSelectionCategory);
    }
    
    function initCourses() {
        initEdit("course");
        $(".remove_course").on("click", removeCourse);
        
        $(".add_ingredient_to_course").on("click", addIngredientToCourse);
        $(".remove_ingredient_from_course").on("click", removeIngredientFromCourse);

        $(".add_selection_to_course").on("click", addSelectionToCourse);
        $(".remove_selection_from_course").on("click", removeSelectionFromCourse);
        
        $(".edit_course_name").on("click", editCourseName);
        $(".edit_course_price").on("click", editCoursePrice);
        $(".edit_course_category").on("click", editCourseCategory);
        $(".edit_course_description").on("click", editCourseDescription);
        
        setupAutocomplete(".course-edit-category-input", categories, "ca_name", "ca_id");
        setupAutocomplete(".ingredient-input", ingredients, "i_name", "i_id");
        setupAutocomplete(".selection-input", selections, "s_name", "s_id");
    }
    
    function initIngredients() {
        initEdit("ingredient");
        $(".remove_ingredient").on("click", removeIngredient);
        
        $(".add_allergene_to_ingredient").on("click", addAllergeneToIngredient);
        $(".remove_allergene_from_ingredient").on("click", removeAllergeneFromIngredient);

        $(".edit_ingredient_name").on("click", editIngredientName);

        setupAutocomplete(".allergene-input", allergenes, "a_name", "a_id");
    }
    
    function initAllergenes() {
        initEdit("allergene");
        $(".remove_allergene").on("click", removeAllergene);

        $(".edit_allergene_name").on("click", editAllergeneName);
    }
    
    function initCategories() {
        initEdit("category");
        $(".remove_category").on("click", removeCategory);  

        $(".edit_category_name").on("click", editCategoryName);
    }
    
    function initSelections() {
        initEdit("selection");
        $(".remove_selection").on("click", removeSelection);

        $(".edit_selection_name").on("click", editSelectionName);

        $(".add_selection_category_to_selection").on("click", addSelectionCategoryToSelection);
        $(".remove_selection_category_from_selection").on("click", removeSelectionCategoryFromSelection);

        setupAutocomplete(".selection-category-input", selectionCategories, "sc_name", "sc_id");
    }
    
    function initSelectionCategories() {
        initEdit("selectionCategory");
        $(".remove_selection_category").on("click", removeSelectionCategory);  

        $(".edit_selection_category_name").on("click", editSelectionCategoryName);
    }

    function initEdit(param) {
        var name = inEdit[param].editName;
        var isEdit = inEdit[param].isEdit;

        for (var i = 0; i < isEdit.length; i++) {
            if (isEdit[i] === true) {
                $(".hidden-default-" + param + "-" + i).css("display", "inline");
                $(".hidden-edit-" + param + "-" + i).css("display", "none");
            } else if (isEdit[i] === false) {
                $(".hidden-default-" + param + "-" + i).css("display", "none");
                $(".hidden-edit-" + param + "-" + i).css("display", "inline");
            }
        }

        $(name).css("display", "inline-block");
        $(name).on("click", function () {
            var id = $(this).prop("name").split("_")[1];
            var idInt = parseInt(id);

            if (isEdit[idInt] === true) {
                $(".hidden-default-" + param + "-" + idInt).css("display", "none");
                $(".hidden-edit-" + param + "-" + idInt).css("display", "inline");
                isEdit[idInt] = false;
            } else {
                $(".hidden-default-" + param + "-" + idInt).css("display", "inline");
                $(".hidden-edit-" + param + "-" + idInt).css("display", "none");
                isEdit[idInt] = true;
            }
        });
    }

    function initModeSwitch() {
        $("#dark-mode").on("click", function() {
            setMode();
            darkMode = true;
        });
        $("#light-mode").on("click", function() {
            setMode();
            darkMode = false;
        });
    }

    /************************\
    | AJAX REQUEST FUNCTIONS | 
    \************************/
        // COURSES
    function addCourse() {
        $.get("/add_course", function (data) {
            $(".course_display").html(data);
            initCourses();
        });
    }

    function removeCourse() {
        var info = $(this).prop("name").split("_");
        if (confirm("Are you sure you want to remove the course '" + info[0] + "'?")) {
            $.get("/remove_course", {c_id: info[1]}, function (data) {
                $(".course_display").html(data);
                initCourses();
            });
        }
    }

    function removeIngredientFromCourse() {
        var info = $(this).prop("name").split("_");
        
        if (confirm("Are you sure you want to remove this ingredient from the course?")) {
            $.get("/remove_ingredient_from_course", {c_id: info[0], i_id: info[1]}, function (data) {
                $(".course_display").html(data);
                initCourses();
            });
        }
    }

    function addIngredientToCourse() {
        var c_id = $(this).prop("id").split("-")[1];
        var i_id = $("#autocomplete_ingredient-" + c_id).prop("name");
        $.get("/add_ingredient_to_course", {c_id: c_id, i_id: i_id}, function (data) {
            $(".course_display").html(data);
            initCourses();
        });
    }

    function addSelectionToCourse() {
        var c_id = $(this).prop("id").split("-")[1];
        var s_id = $("#autocomplete_selection-" + c_id).prop("name");
        $.get("/add_selection_to_course", {c_id: c_id, s_id: s_id}, function (data) {
            $(".course_display").html(data);
            initCourses();
        });
    }
    
    function removeSelectionFromCourse() {
        var info = $(this).prop("name").split("_");
        
        if (confirm("Are you sure you want to remove this selection from the course?")) {
            $.get("/remove_selection_from_course", {c_id: info[0], s_id: info[1]}, function (data) {
                $(".course_display").html(data);
                initCourses();
            });
        }
    }

        // INGREDIENTS
    function addIngredient() {
        $.get("/add_ingredient", function (data) {
            $(".ingredient_display").html(data);
            initIngredients();
            // TODO: Update ingredients list, somehow
        });
    }

    function removeIngredient() {
        var info = $(this).prop("name").split("_");
        if (confirm("Are you sure you want to remove the ingredient '" + info[0] + "'?")) {
            $.get("/remove_ingredient", {i_id: info[1]}, function (data) {
                $(".ingredient_display").html(data);
                initIngredients();
            });
        }
    }

    function addAllergeneToIngredient() {
        var i_id = $(this).prop("id").split("-")[1];
        var a_id = $("#autocomplete_allergene-" + i_id).prop("name");
        $.get("/add_allergene_to_course", {i_id: i_id, a_id: a_id}, function (data) {
            $(".ingredient_display").html(data);
            initIngredients();
        });
    }

    function removeAllergeneFromIngredient() {
        var info = $(this).prop("name").split("_");
        if (confirm("Are you sure you want to remove this allergene from the ingredient?")) {
            $.get("/remove_ingredient_from_course", {i_id: info[0], a_id: info[1]}, function (data) {
                $(".ingredient_display").html(data);
                initIngredients();
            });
        }
    }

        // ALLERGENES

    function addAllergene() {
        $.get("/add_allergene", function (data) {
            $(".allergene_display").html(data);
            initAllergenes();
        });
    }
    
    function removeAllergene() {
        var info = $(this).prop("name").split("_");
        if (confirm("Are you sure you want to remove the allergene '" + info[0] + "'?")) {
            $.get("/remove_allergene", {a_id: info[1]}, function (data) {
                $(".allergene_display").html(data);
                initAllergenes();
            });
        }
    }

        // CATEGORIES

    function addCategory() {
        $.get("/add_category", function (data) {
            $(".category_display").html(data);
            initCategories();
        });
    }
    
    function removeCategory() {
        var info = $(this).prop("name".split("_"));
        if (confirm("Are you sure you want to remove the category '" + info[0] + "'?")) {
            $.get("/remove_category", {c_id: info[1]}, function (data) {
                $(".category_display").html(data);
                initCategories();
            });
        }
    }

        // SELECTIONS

    function addSelection() {
        $.get("/add_selection", function (data) {
            $(".selection_display").html(data);
            initSelections();
        });
    }
    
    function removeSelection() {
        var info = $(this).prop("name".split("_"));
        if (confirm("Are you sure you want to remove the selection '" + info[0] + "'?")) {
            $.get("/remove_selection", {s_id: info[1]}, function (data) {
                $(".selection_display").html(data);
                initSelections();
            });
        }
    }

    function addSelectionCategoryToSelection() {
        var s_id = $(this).prop("id").split("-")[1];
        var sc_id = $("#autocomplete_selection_category-" + s_id).prop("name");
        $.get("/add_selection_category_to_selection", {s_id: s_id, sc_id: sc_id}, function (data) {
            $(".selection_display").html(data);
            initSelections();
        });
    }

    function removeSelectionCategoryFromSelection() {
        var info = $(this).prop("name").split("_");
        if (confirm("Are you sure you want to remove this selection category from the selection?")) {
            $.get("/remove_selection_category_from_selection", {s_id: info[0], sc_id: info[1]}, function (data) {
                $(".selection_display").html(data);
                initSelections();
            });
        }
    }

        // SELECTION CATEGORIES

    function addSelectionCategory() {
        $.get("/add_selection_category", function (data) {
            $(".selection_category_display").html(data);
            initSelectionCategories();
        });
    }

    function removeSelectionCategory() {
        var info = $(this).prop("name".split("_"));
        if (confirm("Are you sure you want to remove the selection category '" + info[0] + "'?")) {
            $.get("/remove_selection_category", {sc_id: info[1]}, function (data) {
                $(".selection_category_display").html(data);
                initSelectionCategories();
            });
        }
    }

    // EDIT FUNCTIONS
        // EDIT COURSE

    function editCourseName() {
        var c_id = $(this).prop("name");
        var c_name = $("#course-edit-name_" + c_id).val();
        $.get("/edit_course_name", {c_id: c_id, c_name: c_name}, function (data) {
            $(".course_display").html(data);
            initCourses();
        });
    }

    function editCoursePrice() {
        var c_id = $(this).prop("name");
        var price = $("#course-edit-price_" + c_id).val();
        $.get("/edit_course_price", {c_id: c_id, price: price}, function (data) {
            $(".course_display").html(data);
            initCourses();
        });
    }

    function editCourseCategory() {
        var c_id = $(this).prop("id").split("-")[1];
        var ca_id = $("#autocomplete_course_edit_category-" + c_id).prop("name");
        $.get("/edit_course_category", {c_id: c_id, ca_id: ca_id}, function (data) {
            $(".course_display").html(data);
            initCourses();
        });
    }

    function editCourseDescription() {
        var c_id = $(this).prop("name");
        var description = $("#course-edit-description_" + c_id).val();
        $.get("/edit_course_description", {c_id: c_id, description: description}, function (data) {
            $(".course_display").html(data);
            initCourses();
        });
    }

        // EDIT INGREDIENTS
    function editIngredientName() {
        var i_id = $(this).prop("name");
        var i_name = $("#ingredient-edit-name_" + i_id).val();
        $.get("/edit_ingredient_name", {i_id: i_id, i_name: i_name}, function (data) {
            $(".ingredient_display").html(data);
            initIngredients();
        });
    }

        // EDIT ALLERGENES
    function editAllergeneName() {
        var a_id = $(this).prop("name");
        var a_name = $("#allergene-edit-name_" + a_id).val();
        $.get("/edit_allergene_name", {a_id: a_id, a_name: a_name}, function (data) {
            $(".allergene_display").html(data);
            initAllergenes();
        });
    }

        // EDIT CATEGORIES
    function editCategoryName() {
        var c_id = $(this).prop("name");
        var c_name = $("#category-edit-name_" + c_id).val();
        $.get("/edit_category_name", {c_id: c_id, c_name: c_name}, function (data) {
            $(".category_display").html(data);
            initCategories();
        });
    }

        // EDIT SELECTIONS
    function editSelectionName() {
        var s_id = $(this).prop("name");
        var s_name = $("#selection-edit-name_" + s_id).val();
        $.get("/edit_selection_name", {s_id: s_id, s_name: s_name}, function (data) {
            $(".selection_display").html(data);
            initSelections();
        });
    }

        // EDIT SELECTION CATEGORIES
    function editSelectionCategoryName() {
        var sc_id = $(this).prop("name");
        var sc_name = $("#selection-category-edit-name_" + sc_id).val();
        $.get("/edit_selection_category_name", {sc_id: sc_id, sc_name: sc_name}, function (data) {
            $(".selection_category_display").html(data);
            initSelectionCategories();
        });
    }


    // I don't know if there are any better solutions for these yet, but these requests
    // have to be synchronous as far as I know in order to work properly.
    function updateIngredients() {
        $.ajax({
            url: "/get_ingredients",
            type: "get",
            async: false,
            success: function(data) {
                ingredients = JSON.parse(data);
            }
        });
    }

    function updateAllergenes() {
        $.ajax({
            url: "/get_allergenes",
            type: "get",
            async: false,
            success: function(data) {
                allergenes = JSON.parse(data);
            }
        });
    }
    
    function updateCategories() {
        $.ajax({
            url: "/get_categories",
            type: "get",
            async: false,
            success: function(data) {
                categories = JSON.parse(data);
            }
        });
    }

    function updateSelections() {
        $.ajax({
            url: "/get_selections",
            type: "get",
            async: false,
            success: function(data) {
                selections = JSON.parse(data);
            }
        });
    }

    function updateSelectionCategories() {
        $.ajax({
            url: "/get_selection_categories",
            type: "get",
            async: false,
            success: function(data) {
                selectionCategories = JSON.parse(data);
            }
        });
    }
});

/*************************\
| MISCELLANIOUS FUNCTIONS | 
\*************************/

function setMode() {
    if (!darkMode) {
        $("#dark-mode").css("display", "none");
        $("#light-mode").css("display", "inline");
        $("table").addClass("table-dark");
        $("input").addClass("bg-dark");
        $("button").addClass("bg-dark");
        $("body").css("background", "#1a1a1a");
        $("h1").css("color", "#ffffff");
        $("h2").css("color", "#ffffff");
        $("h3").css("color", "#ffffff");
        $("h4").css("color", "#ffffff");
        $("h5").css("color", "#ffffff");
        $("h6").css("color", "#ffffff");
        $(".form-control").css("color", "white");
    } else {
        $("#dark-mode").css("display", "inline");
        $("#light-mode").css("display", "none");
        $("table").removeClass("table-dark");
        $("input").removeClass("bg-dark");
        $("button").removeClass("bg-dark");
        $("body").css("background", "#ffffff");
        $("h1").css("color", "#000000");
        $("h2").css("color", "#000000");
        $("h3").css("color", "#000000");
        $("h4").css("color", "#000000");
        $("h5").css("color", "#000000");
        $("h6").css("color", "#000000");
        $(".form-control").css("color", "black");
    }
    $("#light-mode").removeClass("bg-dark");
}

function setupAutocomplete(inputString, dict, nameParamater, idParameter) {
    var inputs = $(inputString);
    for (var i = 0; i < inputs.length; i++) {
        var arrayIn = [];
        for (var j = 0; j < dict.length; j++) {
            arrayIn.push({
                name: dict[j][nameParamater],
                id: dict[j][idParameter] 
            });
        }
        autocomplete(inputs[i], arrayIn);
    }
}

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
            if (arr[i].name.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                b = document.createElement("DIV");
                b.innerHTML = "<strong>" + arr[i].name.substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].name.substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i].name + "'>";
                b.innerHTML += "<input type='hidden' value='" + arr[i].id + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    inp.name = this.getElementsByTagName("input")[1].value;
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