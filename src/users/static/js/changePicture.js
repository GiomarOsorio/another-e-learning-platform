$(document).ready(function () {

    $(".custom-file-input").on("change", function () {
        /**
         * Change value label tag with name of upload element.
         */
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });

    /**
     * Read the data of an element
     * @param {object} element - The element to read
     */
    var readURL = function (input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                crop(e.target.result, $(".avatar"), 1)
            };

            reader.readAsDataURL(input.files[0]);
        }
    };

    /**
     * @param {string} url - The source image
     * @param {string} tag - The tag where draw image
     * @param {number} aspectRatio - The aspect ratio
     */
    function crop(url, tag, aspectRatio) {
        // this image will hold our source image data
        const inputImage = new Image();

        // we want to wait for our image to load
        inputImage.onload = () => {
            // let's store the width and height of our image
            const inputWidth = inputImage.naturalWidth;
            const inputHeight = inputImage.naturalHeight;

            // get the aspect ratio of the input image
            const inputImageAspectRatio = inputWidth / inputHeight;

            // if it's bigger than our target aspect ratio
            let outputWidth = inputWidth;
            let outputHeight = inputHeight;
            if (inputImageAspectRatio > aspectRatio) {
                outputWidth = inputHeight * aspectRatio;
            } else if (inputImageAspectRatio < aspectRatio) {
                outputHeight = inputWidth / aspectRatio;
            }

            // calculate the position to draw the image at
            const outputX = (outputWidth - inputWidth) * 0.5;
            const outputY = (outputHeight - inputHeight) * 0.5;

            // create a canvas that will present the output image
            const outputImage = document.createElement("canvas");

            // set it to the same size as the image
            outputImage.width = outputWidth;
            outputImage.height = outputHeight;

            // draw our image at position 0, 0 on the canvas
            const ctx = outputImage.getContext("2d");
            ctx.drawImage(inputImage, outputX, outputY);

            // draw context canvas in tag
            tag.attr("src", outputImage.toDataURL());
        };

        // start loading our image
        inputImage.src = url;
    }

    $("#id_avatar").on("change", function () {
        /**
         * Add function(readURL) to change event of item with id='id_avatar'
         */
        readURL(this);
    });

});
