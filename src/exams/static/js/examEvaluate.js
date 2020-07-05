$(document).ready(function () {

    /**
     * Return data of Quiz form in a list [Quiz, Questions, Answers]
     */
    function getData() {

        //Variables
        var Questions = {};

        //Questions data
        $('body').find('.card-body').children('.card-question').each(function (index) {
            var questionIndex = 'Question' + (index++)
            Questions[questionIndex] = {
                'id': $(this).attr('data-id'),
            };

            //Answer data
            Answer = [];
            // document.querySelector("#formquestion > div:nth-child(2) > p > label > input")
            $(this).find('.form-check').each(function (index) {
                Answer.push([$(this).find('input[name="answer"]').attr('data-id'), $(this).find('input[name="answer"]').is(":checked")]);
            });
            Questions[questionIndex]['Answers'] = Answer
        });
        return Questions
    };

    /**
     * Send a request to the server to evaluate the quiz, add security X-CSRFToken
     * @param {object} data - The data to send
     */
    function sendData(data) {
        $.ajax({
            async: false,
            type: 'POST',
            url: window.location.pathname,
            headers: {
                "X-CSRFToken": $('#button-controls input[name="csrfmiddlewaretoken"]').attr('value'),
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({
                'Questions': data,
            }),
            success: function (JSONdata) {
                var urlData = JSON.parse(JSONdata)
                if (urlData.url) {
                    console.log('success evaluated!')
                    window.location.href = window.location.origin + urlData.url;
                } else {
                    console.log('error, please contact the administrator')
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ":" + xhr.responseText);
                console.log(data)
            }
        });
    };

    $('#exam-evaluate').on("click", function (e) {
        /*
        Get data of Quiz, send to and evaluate it.
        */
        $(this).find(".fa").toggleClass("fa-refresh fa-spin");
        sendData(getData());
    });

});
