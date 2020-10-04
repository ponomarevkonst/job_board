$(document).ready(function() {
    var reader = new FileReader();
    reader.onload = function (e) {
        $('#logo').attr('src', e.target.result);
    }

    function readURL(input) {
        if (input.files && input.files[0]) {
            reader.readAsDataURL(input.files[0]);
        }
    }

    $(".custom-file-input").change(function () {
        readURL(this);
    });
});