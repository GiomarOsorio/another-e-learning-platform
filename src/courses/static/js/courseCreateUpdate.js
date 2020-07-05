$(document).ready(function () {

    /*
    variable that stores tags and banner_base64 
    */
    var banner_base64 = '';
    var tags = [];
    var what_learn = [];

    /**
     * Find the closest element and remove it with animation 'slow'.
     * @param {object} element - The principal element.
     * @param {object} closest_element - The element to find and remove it.
     */
    function delClosest(element, closest_element) {
        event.preventDefault();
        element.closest(closest_element).hide('slow', function () { element.closest(closest_element).remove(); });
    };

    /**
     * Find the element and scroll to it if exist, with animation 'linear'.
     * @param {object} element - The element to jump it.
     * @param {event} e - The event.
     */
    function jumpTO(element, e) {
        if (element.length) {
            e.preventDefault();
            $('html, body').animate({
                scrollTop: element.offset().top
            }, 1000,
                'linear'
            );
        }

    };

    /**
     * Find child element of parent element of trggr with class content and remove it, add element depending on value of element trggr.
     * @param {object} trggr - The select tag element.
     */
    function toogleContent(trggr) {
        $(trggr).closest('.containercontent').find('.content').remove();
        var element = $('');
        switch (trggr.value) {
            case '1':
                element = $('<div class="col-8 col-sm-8 px-0 content"><textarea placeholder="Enter text in plain text format" autocomplete required class="form-control form-control-lg contentdata"></textarea></div>')
                break;
            case '2':
                element = $('<div class="col-8 col-sm-8 px-0 content"><textarea placeholder="Enter text in HTML format" autocomplete required class="form-control form-control-lg contentdata"></textarea></div>')
                break;
            case '3':
                element = $('<div class="col-8 col-sm-8 px-0 content"><input placeholder="Enter URL of video" autocomplete required class="form-control form-control-lg contentdata"></div>')
                break;
            case '4':
                element = $('<div class="col-8 col-sm-8 px-0 content"><input placeholder="Enter URL of document" autocomplete required class="form-control form-control-lg contentdata"></div>')
                break;
            case '5':
                element = $('#exams-template').contents().clone(true, true);
                if ($(trggr).closest('div').find('#exam_data').length == 1) {
                    exam_id = $(trggr).closest('div').find('#exam_data').data('id');
                    exam_name = $(trggr).closest('div').find('#exam_data').val();
                    element.find('.contentdata option').eq(0).remove()
                    element.find('.contentdata option').eq(0).before($("<option selected></option>").val(exam_id).text(exam_name));
                }
                break;
            default:
                alert('content type is undefined');
        }
        $(trggr).closest('.containercontent').append(element)
    }

    /**
     * Add events to buttons that don't have them. Use in update data
     */
    function addDel() {
        var dellWhatLearnsButtons = $('body').find('#what_learns').find('.close.btn');
        var delTagsButtons = $('body').find('#learn_tags').find('.close.btn');

        var delModulesButtons = $('body').find('.del-module');

        var addSegmentsButtons = $('body').find('.add-segment');
        var delSegmentsButtons = $('body').find('.del-segment');

        var addContentsButtons = $('body').find('.add-content');
        var delContentsButtons = $('body').find('.del-content');

        var toogleContentButtons = $('body').find('.id_content_type');

        for (let i = 0; i < dellWhatLearnsButtons.length; i++) {
            var inputWhatLearn = $(dellWhatLearnsButtons[i]).parent().find('span')[1].innerText;
            what_learn.push(inputWhatLearn);

            dellWhatLearnsButtons[i].onclick = function () {
                var inputWhatLearn = $(this).parent().find('span')[1].innerText;
                delClosest($(this), ".btn-group");
                const index = what_learn.indexOf(inputWhatLearn);
                if (index > -1) {
                    what_learn.splice(index, 1);
                }
            };

        };
        for (let i = 0; i < delTagsButtons.length; i++) {
            var inputLearnTag = $(delTagsButtons[i]).parent().find('span')[1].innerText;
            tags.push(inputLearnTag);

            delTagsButtons[i].onclick = function () {
                var inputLearnTag = $(this).parent().find('span')[1].innerText;
                delClosest($(this), ".btn-group");
                const index = tags.indexOf(inputLearnTag);
                if (index > -1) {
                    tags.splice(index, 1);
                }
            };
        };

        for (let i = 0; i < delModulesButtons.length; i++) {
            delModulesButtons[i].onclick = function () { delClosest($(this), ".containermodule"); };
        };

        for (let i = 0; i < addSegmentsButtons.length; i++) {
            addSegmentsButtons[i].onclick = function () { getAndCloneSegment($(this), $(this).closest('.containermodule'), '#segment-template', '#content-template'); };
        };
        for (let i = 0; i < delSegmentsButtons.length; i++) {
            delSegmentsButtons[i].onclick = function () { delClosest($(this), '.containersegment'); };
        };

        for (let i = 0; i < addContentsButtons.length; i++) {
            addContentsButtons[i].onclick = function () { getAndCloneContent($(this), $(this).closest('.containersegment'), '#content-template'); };
        };
        for (let i = 0; i < delContentsButtons.length; i++) {
            delContentsButtons[i].onclick = function () { delClosest($(this), '.form-containercontent'); };
        };

        for (let i = 0; i < toogleContentButtons.length; i++) {
            toogleContentButtons[i].onchange = function () { toogleContent(this); };
        };

    };

    /**
     * Clone the template id='content-template', add corresponding events to buttons and insert it in html
     * @param {object} tmpltS - The segment element where insert content element.
     * @param {string} tmpltC - The template id content.
     * @param {number} newid - the data-id of the content to insert.
     */
    function cloneContent(tmpltS, tmpltC, newid) {
        tContent = $(tmpltC).contents().clone(true, true);
        tContent.attr('data-id', newid);

        var delbutton = tContent.find('.del-content');
        delbutton.on('click', function () {
            delClosest($(this), '.form-containercontent');
        });

        var typecontentbutton = tContent.find('.id_content_type');
        typecontentbutton.on('change', function () {
            toogleContent(this)
        });

        tContent.insertBefore(tmpltS.find('#div-addcontent'));
    };


    /**
     * Manages the number of answer in the form assigning corresponding ip and calling the answer cloner.
     * @param {object} trgt - button trigger of add content.
     * @param {object} tmpltS - The segment element where insert content element.
     * @param {string} tmpltC - The template id content.
     */
    function getAndCloneContent(trgt, tmpltS, tmpltC) {
        var new_content_id = 0;
        var form_content = trgt.closest(".containersegment");

        form_content.find('.form-containercontent').each(function (index) {
            if (parseInt($(this).data('id'))) {
                new_content_id = $(this).data('id');
            }
        });

        new_content_id++;
        cloneContent(tmpltS, tmpltC, new_content_id);
    };

    /**
     * Clone the template id='segment-template', add corresponding events to buttons and insert it in html
     * @param {object} tmpltM - The module element where insert segment element.
     * @param {string} tmpltS - The template id segment
     * @param {string} tmpltC - The template id content.
     * @param {number} newid - the data-id of the segment to insert.
     */
    function cloneSegment(tmpltM, tmpltS, tmpltC, newid) {
        var tSegment = $(tmpltS).contents().clone(true, true);
        tSegment.attr('id', 'card-segment-' + newid);
        tSegment.attr('data-id', newid);

        var delbutton = tSegment.find('.del-segment');
        delbutton.on('click', function () {
            delClosest($(this), '.containersegment');
        });

        var addcontentbutton = tSegment.find('.add-content');
        addcontentbutton.on('click', function () {
            getAndCloneContent($(this), tSegment, tmpltC);
        });

        addcontentbutton.trigger("click");

        tSegment.insertBefore(tmpltM.find('hr'));
    };

    /**
     * Manages the number of answer in the form assigning corresponding id and calling the answer cloner.
     * @param {number} trgt - button trigger of add segment.
     * @param {object} tmpltM - The module element where insert segment element.
     * @param {string} tmpltS - The template id segment
     * @param {string} tmpltC - The template id content.
     */
    function getAndCloneSegment(trgt, tmpltM, tmpltS, tmpltC) {
        var new_segment_id = 0;
        var form_segment = trgt.closest(".form-segments");

        form_segment.find('.containersegment').each(function (index) {
            if (parseInt($(this).data('id'))) {
                new_segment_id = $(this).data('id');
            }
        });

        new_segment_id++;
        cloneSegment(tmpltM, tmpltS, tmpltC, new_segment_id);
    };

    /**
     * Clone the template id='module-template', add corresponding events to buttons and insert it in html.
     * @param {number} trgt - button trigger of add module.
     * @param {object} tmpltM -  The template id module.
     * @param {number} newid - the data-id of the module to insert.
     * @param {string} tmpltS - The template id segment
     * @param {string} tmpltC - The template id content.
     */
    function cloneModule(trgt, tmpltM, newid, tmpltS, tmpltC) {

        var tModule = $(tmpltM).contents().clone(true, true);
        tModule.attr('id', 'card-module-' + newid);
        tModule.attr('data-id', newid);

        var addsegmentbutton = tModule.find('.add-segment');
        addsegmentbutton.on('click', function () {
            getAndCloneSegment($(this), tModule, tmpltS, tmpltC);
        });

        var delmodulebutton = tModule.find('.del-module');
        delmodulebutton.on('click', function () {
            delClosest($(this), ".containermodule");
        });

        addsegmentbutton.trigger("click");

        tModule.insertBefore(trgt.closest('#button-controls'));
    };

    /**
     * Manages the number of modules in the form assigning corresponding id and calling the module cloner.
     * @param {number} trgt - button trigger of add module.
     * @param {event} e - The event.
     * @param {object} tmpltM -  The template id module.
     * @param {string} tmpltS - The template id segment
     * @param {string} tmpltC - The template id content.
     */
    function getAndCloneModule(trgt, e, tmpltM, tmpltS, tmpltC) {
        var new_module_id = 0;
        var card_module = $("body").find(".containermodule");

        card_module.each(function (index) {
            if (parseInt($(this).data('id')) > new_module_id) {
                new_module_id = $(this).data('id');
            }
        });

        new_module_id++;
        cloneModule(trgt, tmpltM, new_module_id, tmpltS, tmpltC);
        jumpToElement = $('#card-module-' + new_module_id.toString())
        if (new_module_id > 1 && jumpToElement) {
            setTimeout(function () {
                jumpTO(jumpToElement, e);
            }, 400);
        }
    };

    /**
     * Read the data of an element
     * @param {object} input - The element to read
     */
    var readURL = function (input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                banner_base64 = e.target.result;
            };

            reader.readAsDataURL(input.files[0]);
        }
    };

    /**
     * Get data of Course form and return it in an variable "Course"
     */
    function getData() {

        //Variables
        var Course = {}
        var Modules = {};
        var Segment = {};
        var Content = {};

        //Course data        
        var html_course = $('body').find('#course_form');
        Course['user'] = $('#button-controls input[name="user"]').attr('value');
        Course['name'] = html_course.find('#id_name_course').val();
        Course['description'] = html_course.find('#id_description').val();
        Course['banner'] = banner_base64;
        Course['tags'] = (tags.length > 0) ? tags.join('%20') : '';
        Course['what_learn'] = (what_learn.length > 0) ? what_learn.join('%20') : '';


        //Modules data
        $('body').find('.containermodule').each(function (index) {
            var moduleIndex = 'Module' + (index++)
            Modules[moduleIndex] = {
                'name': $(this).find('input.id_name').val(),
            };

            //Segments data
            Segment = {};
            $(this).find('.containersegment').each(function (index) {
                segmentIndex = 'Segment' + (index++)
                Segment[segmentIndex] = {
                    'name': $(this).find('.id_name').val(),
                };

                //Contents data
                Content = {};
                $(this).find('.containercontent').each(function (index) {
                    contentIndex = 'Content' + (index++);
                    Content[contentIndex] = {
                        'name': $(this).parent().find('.contentname').val(),
                        'content_type': $(this).find('.id_content_type').val(),
                        'content': $(this).find('.contentdata').val(),
                    };

                });
                Segment[segmentIndex]['Contents'] = Content;
            });
            Modules[moduleIndex]['Segments'] = Segment;
        });
        Course['Modules'] = Modules

        return Course
    };

    /**
     * Send a request to the server to save the Course, add security X-CSRFToken
     * @param {object} data - The data to send 
     */
    function sendData(data) {
        $.ajax({
            async: true,
            type: 'POST',
            url: window.location.pathname,
            headers: {
                "X-CSRFToken": $('#button-controls input[name="csrfmiddlewaretoken"]').attr('value'),
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({
                'Course': data,
            }),
            success: function (JSONdata) {
                var data = JSON.parse(JSONdata)
                if (data.error) {
                    $('body').html(data.content);
                    tags.forEach(function (item, index) {
                        var tagHTML = $(`
                        <div class="btn-group" role="group">
                            <a type="button" class="close btn pr-0 text-muted m-auto" style="font-size: 0.875rem; padding: 0.1875rem 1.125rem;" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </a>
                            <span class="btn pl-0 text-dark" style="font-size: 0.875rem; padding: 0.1875rem 1.125rem; margin: .5rem!important;">
                                `+ item + `
                            </span>
                        </div>`);
                        tagHTML.find('a').on("click", function () {
                            delClosest($(this), ".btn-group");
                            if (tags.indexOf(item) > -1) {
                                tags.splice(tags.indexOf(item), 1);
                            }
                        });
                        $('#learn_tags').append(tagHTML);
                    });
                    what_learn.forEach(function (item, index) {
                        var what_learnHTML = $(`
                        <div class="btn-group" role="group">
                            <a type="button" class="close btn pr-0 text-mute m-auto" style="font-size: 0.875rem; padding: 0.1875rem 1.125rem;" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </a>
                            <span class="pl-0 text-dark col text-left text-wrap" style="font-size: 0.875rem; padding: 0.1875rem 1.125rem; margin: .5rem!important;">`
                            + item +
                            `</span>
                        </div>`);
                        what_learnHTML.width($('#what_learns').width());


                        what_learnHTML.find('a').on("click", function () {
                            delClosest($(this), ".btn-group");
                            if (what_learn.indexOf(item) > -1) {
                                what_learn.splice(what_learn.indexOf(item), 1);
                            }
                        });
                        $('#what_learns').append(what_learnHTML);
                    });
                } else {
                    window.location.href = window.location.origin + data.url_redirect;
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ":" + xhr.responseText);
                console.log(data)
            }
        });
    };

    /**
     * Manage tags "Learns" add Tags to html and append to tags, and verified if exist
     * @param {object} trggr - The element trigger of add tag
     */
    function tagsData(trggr) {
        var inputLearnTag = trggr.closest('#div-tags').find('input').val();
        const index = tags.indexOf(inputLearnTag);
        if (index == -1) {
            $('#exist_tag').remove();
            tags.push(inputLearnTag);

            var tag = $(`
            <div class="btn-group" role="group">
                <a type="button" class="close btn pr-0 text-muted m-auto" style="font-size: 0.875rem; padding: 0.1875rem 1.125rem;" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </a>
                <span class="btn pl-0 text-dark" style="font-size: 0.875rem; padding: 0.1875rem 1.125rem; margin: .5rem!important;">
                    `+ inputLearnTag + `
                </span>
            </div>`)
            tag.find('a').on("click", function () {
                delClosest($(this), ".btn-group");
                if (tags.indexOf(inputLearnTag) > -1) {
                    tags.splice(tags.indexOf(inputLearnTag), 1);
                }
            });

            $('#learn_tags').append(tag);
            trggr.closest('#div-tags').find('input').val('');
        } else {
            if ($("#exist_tag").length == 0) {
                $('<small id="exist_tag" class="alert-danger">ya existe un tag con ese nombre</small>').insertBefore($('#learn_tags'));
            }
        }
    };

    /**
     * Manage tags "What Learn" add Tags to html and append to tags, and verified if exist
     * @param {object} trggr - The element trigger of add tag
     */
    function whatLearnData(trggr) {
        var inputWhatLearn = trggr.closest('#div-what_learn').find('textarea').val();
        const index = what_learn.indexOf(inputWhatLearn);
        if (index == -1) {
            $('#exist_what_learn').remove();
            what_learn.push(inputWhatLearn);

            var tag = $(`
                <div class="btn-group" role="group">
                    <a type="button" class="close btn pr-0 text-mute m-auto" style="font-size: 0.875rem; padding: 0.1875rem 1.125rem;" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </a>
                    <span class="pl-0 text-dark col text-left text-wrap" style="font-size: 0.875rem; padding: 0.1875rem 1.125rem; margin: .5rem!important;">`
                + inputWhatLearn +
                `</span>
                </div>`);
            tag.width($('#what_learns').width());

            tag.find('a').on("click", function () {
                delClosest($(this), ".btn-group");
                if (what_learn.indexOf(inputWhatLearn) > -1) {
                    what_learn.splice(what_learn.indexOf(inputWhatLearn), 1);
                }
            });

            $('#what_learns').append(tag);
            trggr.closest('#div-what-your-learn').find('textarea').val('');
        } else {
            if ($("#exist_what_learn").length == 0) {
                $('<small id="exist_what_learn" class="alert-danger">ya existe una caracteristica igual</small>').insertBefore($('#what_learns'));
            }

        }
    };

    $(".custom-file-input").on("change", function () {
        /**
         * Change value label tag with name of upload element.
         */
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });


    $('#addwhat_learn').on("click", function (e) {
        /**
         * Add function(whatLearnData) to click event of item with id='addwhat_learn'
         */
        whatLearnData($(this));
    });


    $('#addtags').on("click", function (e) {
        /**
         * Add function(tagsData) to click event of item with id='addtags'
         */
        tagsData($(this));
    });


    $('#create-module').on("click", function (e) {
        /**
         * Add function(getAndCloneModule) to click event of item with id='create-module'
         */
        getAndCloneModule($(this), e, '#module-template', '#segment-template', '#content-template');
    });


    $('#create-course').on("click", function (e) {
        /**
         * Add function(sendData) to click event of item with id='create-course'
         */
        $(this).find(".fa").toggleClass("fa-refresh fa-spin");
        sendData(getData());
    });


    /*
    if the form not has modules trigger addDel(),
    otherwise trigger click button id='create-module'
    */
    if ($('#button-controls input[name="hasModule"]').attr('value') == 'False') {
        $('#create-module').trigger("click");
    } else {
        addDel();
    };

    $("#id_banner").on("change", function () {
        /**
         * Add function(readURL) to change event of item with id='id_banner'
         */
        readURL(this);
    });
});
