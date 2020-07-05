$(window).on('load', function (e) {
    /**
     * Add function(viewUpdate), and manage specific event of elements like:
     *   ".course-list"
     *   "#navbar-toggler.modules-menu"
     *   ".btn-chevronicon-dp"
     *   ".btn-chevronicon-rl"
     *   "#display-modules"
     *   "#display-module"
     *  in to window event 'load'
    */

    viewUpdate($(window).width());

    if ($(".course-list").length && $(".exam-list").length) {
        toggleIconDP($(".course-list"), $(".exam-list"));
    };

    if ($("#navbar-toggler.modules-menu").length) {
        $("#navbar-toggler.modules-menu").on('click', function (e) {
            toggleModulesMenu($("#navbar-toggler.modules-menu"), $("#modules-menu"), $("#course"));
        });
    };

    if ($(".btn-chevronicon-dp").length) {
        chevronButtonsParent = $(".btn-chevronicon-dp")
        chevronButtonsParent.each(function () {
            $(this).on('click', function () {
                toggleChevronDP($(this).find(".chevronicon"));
            });
        });
    }

    if ($(".btn-chevronicon-rl").length) {
        chevronButtonsParent = $(".btn-chevronicon-rl")
        chevronButtonsParent.each(function () {
            $(this).on('click', function () {
                toggleChevronDP($(this).find(".chevronicon"));
            });
        });
    }

    if ($("#display-modules").length) {
        $("#display-modules").on('click', function () {
            $("#module").fadeTo('slow', 0.00, function () {
                $("#module").hide();
                $("#modules").show();
                $("#modules").fadeTo('slow', 100.00);
            });
        });
    };
    if ($("#display-module").length) {
        $("#display-module").on('click', function () {
            $("#modules").fadeTo('slow', 0.00, function () {
                $("#modules").hide();
                $("#module").show();
                $("#module").fadeTo('slow', 100.00);
            });
        });
    };

});

$(window).on('resize', function (e) {
    /**
     * Add function(viewUpdate) to window event 'resize'
    */
    viewUpdate($(window).width());
});

/**
 * Manage dropdown menu in responsive mode.
 * @param {string} trigger - The element trigger of show/hide element.
 * @param {string} target - The element to show.
 * @param {string} target2 - The element to hide.
 */
function toggleModulesMenu(trigger, target, target2) {
    $(trigger).addClass("disabled");
    $(trigger).prop("disabled", true)
    if ($(trigger).hasClass("hid")) {
        $(target2).hide('slow', function () { $(target).show(700); });
        $(trigger).removeClass("hid ml-2");
        $(trigger).find("i").removeClass("fa-chevron-right").addClass("fa-chevron-left");
    } else {
        $(target).hide('slow', function () { $(target2).show(700); });
        $(trigger).addClass("hid ml-2");
        $(trigger).find("i").removeClass("fa-chevron-left").addClass("fa-chevron-right");
    };
    setTimeout(function () {
        $(trigger).removeClass("disabled");
        $(trigger).prop("disabled", false);
    }, 1500);
};

/**
 * Toogle class (fa-chevron-down and fa-chevron-up).
 * @param {string} target - The parent of "i" element to toggle class.
 */

function toggleChevronDP(target) {
    if (target.find("i").hasClass("fa-chevron-down")) {
        target.find("i").removeClass("fa-chevron-down").addClass("fa-chevron-up");
    } else {
        target.find("i").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    };
};

/**
 * Toogle class (fa-chevron-right and fa-chevron-left).
 * @param {string} target - The parent of "i" element to toggle class.
 */
function toggleChevronRL(target) {
    if (target.find("i").hasClass("fa-chevron-right")) {
        target.find("i").removeClass("fa-chevron-right").addClass("fa-chevron-left");
    } else {
        target.find("i").removeClass("fa-chevron-left").addClass("fa-chevron-right");
    };
};

/**
 * Add event(toggleChevronDP) on click of elements.
 * @param {object} buttonsCourseAction - The element to add event.
 * @param {object} buttonsExamAction - The element to add event.
 */
function toggleIconDP(buttonsCourseAction, buttonsExamAction) {

    buttonsCourseAction.each(function () {
        $(this).on('click', function () {
            toggleChevronDP($(this));
        });
    });

    buttonsExamAction.each(function () {
        $(this).on('click', function () {
            toggleChevronDP($(this));
        });
    });
};

/**
 * Manage responsive of elements with js.
 * @param {object} viewportWidth - The width of viewport.
 */
function viewUpdate(viewportWidth) {
    if (viewportWidth > 767.98) {

        //navbar
        //toogle name nav-brand
        if ($('.navbar-brand').text() == "AE-LP") {
            $('.navbar-brand').text("Another E-Learning Platform")
        }
        //toogle class search form
        if ($("#navbarResponsive > form.input-group").length) {
            $("#navbarResponsive > form").removeClass("input-group").addClass("form-inline");
        };

        //content
        //toogle class btn
        if ($(".btn-responsive.btn-sm.btn-lg").length) {
            $(".btn-responsive").removeClass("btn-sm btn-lg").addClass("btn-md");
        }
        //display element id=modules-menu
        if ($("#modules-menu").length) {
            $("#course").show();
            if ($("#modules-menu").css("display") == "none") {
                $("#modules-menu").show();
                $("#navbar-toggler.modules-menu").removeClass("hid ml-2")
            };
        };
        //title course toggle
        if ($("#courseTitle").length) {
            $("#courseTitle").removeClass("h3").addClass("h1");
        };

        //footer
        // toogle class footer name 
        if ($("#sticky-footer").find("p.h6").length) {
            footerName = $("#sticky-footer").find("p.h6");
            footerName.removeClass("h6 pl-2").addClass("h4");
        };
        // toogle github icon
        if ($("#githubIcon.pl-1.pr-2").length) {
            $("#githubIcon").removeClass("pl-1 pr-2").addClass("pl-3");
        };
    } else if (viewportWidth > 575.98) {

        //navbar
        //toogle name nav-brand
        if ($('.navbar-brand').text() == "Another E-Learning Platform") {
            $('.navbar-brand').text("AE-LP")
        }
        //toogle class search form
        if ($("#navbarResponsive > form.form-inline").length) {
            $("#navbarResponsive > form").removeClass("form-inline").addClass("input-group");
        };

        //content
        //toogle class btn
        if ($(".btn-responsive.btn-xs.btn-md").length) {
            $(".btn-responsive").removeClass("btn-xs btn-md").addClass("btn-sm");
        }
        //hide element id=modules-menu
        if ($("#modules-menu").length) {
            if ($("#modules-menu").css("display") == "block" && $("#course").css("display") == "block") {
                $("#modules-menu").hide();
                $("#navbar-toggler.modules-menu").addClass("hid ml-2")
            };
        };
        //title course toggle
        if ($("#courseTitle").length) {
            $("#courseTitle").removeClass("h1").addClass("h3");
        };

        //footer
        // toogle footer name 
        if ($("#sticky-footer").find("p.h4").length) {
            footerName = $("#sticky-footer").find("p.h4");
            footerName.removeClass("h4").addClass("h6 pl-2");
        }
        // toogle github icon
        if ($("a#githubIcon.pl-3").length) {
            $("#githubIcon").removeClass("pl-3").addClass("pl-1 pr-2");
        };

    } else {

        //navbar
        //toogle name nav-brand
        if ($('.navbar-brand').text() == "Another E-Learning Platform") {
            $('.navbar-brand').text("AE-LP")
        }
        //toogle class search form
        if ($("#navbarResponsive > form.form-inline").length) {
            $("#navbarResponsive > form").removeClass("form-inline").addClass("input-group");
        };

        //content
        //add class to btn
        $(".btn-responsive").addClass("btn-sm");
        //hide element id=modules-menu
        if ($("#modules-menu").length) {
            if ($("#modules-menu").css("display") == "block" && $("#course").css("display") == "block") {
                $("#modules-menu").hide();
                $("#navbar-toggler.modules-menu").addClass("hid ml-2")
            };
        };
        //title course toggle
        if ($("#courseTitle").length) {
            $("#courseTitle").removeClass("h1").addClass("h3");
        };

        //footer
        // toogle footer name 
        if ($("#sticky-footer").find("p.h4").length) {
            footerName = $("#sticky-footer").find("p.h4");
            footerName.removeClass("h4").addClass("h6 pl-2");
        }
        // toogle github icon
        if ($("a#githubIcon.pl-3").length) {
            $("#githubIcon").removeClass("pl-3").addClass("pl-1 pr-2");
        };

    };
}
