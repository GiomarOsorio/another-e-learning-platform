$(document).ready(function () {

    /**
     * Find the closest element and remove it with animation 'slow'.
     * @param {object} element - The principal element.
     * @param {object} closest_element - The element to find and remove it.
     */
    function delClosest(element, trgt) {
        element.closest(closest_element).hide('slow', function () { element.closest(closest_element).remove(); });
    };

    /**
     * Find the element and scroll to it if exist, with animation 'linear'.
     * @param {object} element - The element to jump it.
     * @param {event} e - The event.
     */
    function jumpTo(trgt, e) {
        if (trgt.length) {
            e.preventDefault();
            e.stopPropagation();
            $('html, body').animate({
                scrollTop: trgt.offset().top
            }, 750,
                'linear'
            );
        }
    };

    /**
     * Clone the template id='question-template', add corresponding events to buttons and insert it in html
     * @param {object} trgt - button trigger of add question.
     * @param {string} tmpltQ - The template id question.
     * @param {number} newid - the data-id of the question to insert.
     * @param {string} tmpltA - The template id answer.
     */
    function cloneQuestion(trgt, tmpltQ, newid, tmpltA) {
        var tQuestion = $(tmpltQ).contents().clone(true, true);
        tQuestion.attr('id', 'card-question-' + newid);
        tQuestion.attr('data-id', newid);

        var addanswerbutton = tQuestion.find('.add-answer');
        addanswerbutton.on('click', function () {
            getAndCloneAnswer($(this), tQuestion, tmpltA);
        });

        var delquestionbutton = tQuestion.find('.del-question');
        delquestionbutton.on('click', function () {
            delClosest($(this), ".card-question");
        });

        addanswerbutton.trigger("click");
        addanswerbutton.trigger("click");

        tQuestion.insertBefore(trgt.closest('#button-controls'));
    };

    /**
     * Manages the number of questions in the form assigning corresponding ip and calling the answer cloner.
     * @param {object} trgt - button trigger of add question.
     * @param {event} e - The event.
     * @param {string} tmpltQ - The template id question.
     * @param {string} tmpltA - The template id answer.
     */
    function getAndCloneQuestion(trgt, e, tmpltQ, tmpltA) {

        var new_question_id = 0;
        var card_body = $("body").find(".card-question");

        card_body.each(function (index) {
            if (parseInt($(this).data('id')) > new_question_id) {
                new_question_id = $(this).data('id');
            }
        });

        new_question_id++;
        cloneQuestion(trgt, tmpltQ, new_question_id, tmpltA);
        jumpToElement = $('#card-question-' + new_question_id.toString())
        if (new_question_id > 1 && jumpToElement) {
            setTimeout(function () {
                jumpTo(jumpToElement, e);
            }, 100);
        }
    };

    /**
     * Clone the template id='answer-template', add corresponding events to buttons and insert it in html
     * @param {string} tmpltQ - The template id question.
     * @param {string} tmpltA - The template id answer.
     * @param {number} newid - the data-id of the segment to insert.
     */
    function cloneAnswer(tmpltQ, tmpltA, newid) {
        tAnswer = $(tmpltA).contents().clone(true, true);
        tAnswer.attr('id', 'card-answer-' + newid);
        //tAnswer.attr('data-id',newid);

        var delbutton = tAnswer.find('.del');
        delbutton.on('click', function () {
            delClosest($(this), '.containeranswer');
        });

        tAnswer.insertBefore(tmpltQ.find('#div-addanswer'));
    };

    /**
     * Manages the number of answer in the form assigning corresponding ip and calling the answer cloner.
     * @param {object} trgt - button trigger of add answer.
     * @param {string} tmpltQ - The template id question.
     * @param {string} tmpltA - The template id answer.
     */
    function getAndCloneAnswer(trgt, tmpltQ, tmpltA) {
        var new_answer_id = 0;
        var form_answer = trgt.closest("#form-answers");

        form_answer.find('.containeranswer').each(function (index) {
            if (parseInt($(this).data('id'))) {
                new_answer_id = $(this).data('id');
            }
        });

        new_answer_id++;
        cloneAnswer(tmpltQ, tmpltA, new_answer_id);
    };

    /**
     * Add events to buttons that don't have them. Use in update data
     */
    function addDel() {
        /*
        Add function(delClosest) to click event of item with class='del-question'
        Add function(delClosest) to click event of item with class='del'
        Add function(getAndCloneAnswer) to click event of item with class='add-question'
        */
        var delQuestionsButtons = $('body').find('.del-question');
        var delAnswersButtons = $('body').find('.del');
        var addAnswersButtons = $('body').find('.add-answer');
        for (let i = 0; i < delQuestionsButtons.length; i++) {
            delQuestionsButtons[i].onclick = function () { delClosest($(this), ".card-question"); };
        };
        for (let i = 0; i < delAnswersButtons.length; i++) {
            delAnswersButtons[i].onclick = function () { delClosest($(this), '.containeranswer'); };
        };
        for (let i = 0; i < addAnswersButtons.length; i++) {
            addAnswersButtons[i].onclick = function () { getAndCloneAnswer($(this), $(this).closest('#form-answers'), '#answer-template'); };
        };
    };

    /**
     * Get data of Exam form and return it in an variable "Exam"
     */
    function getData() {

        //Variables
        var Exam = {}
        var Questions = {};
        var Answers = {};

        //Exam data
        var html_exam = $('body').find('#exam_form');
        Exam['name'] = html_exam.find('#id_name').val();
        Exam['description'] = html_exam.find('#id_description').val();
        Exam['approved'] = html_exam.find('#id_approved').val();

        //Questions data
        $('body').find('.card-question').each(function (index) {
            console.log()
            var questionIndex = 'Question' + (index++)
            Questions[questionIndex] = {
                'question': $(this).find('input#id_question').val(),
                'correct_answers': 0,
                'question_value': $(this).find('input#id_question_value').val(),
            };

            //Answer data
            Answers = {};
            $(this).find('.containeranswer').each(function (index) {
                var AnswerIndex = 'Answer' + (index++)
                Answers[AnswerIndex] = {
                    'answer': $(this).find('.answer').val(),
                    'correct_answer': $(this).find('.correct_answer').is(":checked"),
                };
                Questions[questionIndex]['correct_answers'] = (Answers[AnswerIndex]['correct_answer'] == true) ? Questions[questionIndex]['correct_answers'] + 1 : Questions[questionIndex]['correct_answers'];
            });
            Questions[questionIndex]['Answers'] = Answers;
        });
        Exam['Questions'] = Questions

        return Exam
    };

    /**
     * Send a request to the server to save the quiz, add security X-CSRFToken
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
                'Exam': data,
            }),
            success: function (JSONdata) {
                var data = JSON.parse(JSONdata)
                if (data.error) {
                    $('body').html(data.content);
                } else {
                    window.location.href = window.location.origin + data.url_redirect;
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ":" + xhr.responseText);
            }
        });
    };


    $('#create-question').on("click", function (e) {
        /*
        Add function(getAndCloneQuestion) to click event of item with id='create-question'
        */
        getAndCloneQuestion($(this), e, '#question-template', '#answer-template');
    });


    $('#update-exam').on("click", function (e) {
        /*
        Add function(sendData) to click event of item with id='update-exam'
        */
        $(this).find(".fa").toggleClass("fa-refresh fa-spin");
        data = getData()
        console.log('hola')
        console.log(data);
        sendData(getData());
    });

    $('#create-exam').on("click", function (e) {
        /*
        Add function(sendData) to click event of item with id='update-exam'
        */
        $(this).find(".fa").toggleClass("fa-refresh fa-spin");
        data = getData()
        console.log('hola')
        console.log(data);
        sendData(data);
    });

    /*
    if the form not has modules trigger addDel(),
    otherwise trigger click button id='create-question'
    */
    if ($('#button-controls input[name="hasModule"]').attr('value') == 'False') {
        $("#create-question").trigger("click");
    } else {
        addDel();
    };
});