function showHidePass() {
    var x = document.getElementById("password"); // Use the correct id here
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result)
                .width(150)
                .height(200);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function uploadImage() {
    var fileInput = document.getElementById('imageInput');
    var file = fileInput.files[0];

    var formData = new FormData();
    formData.append('image', file);

    // Add other form fields to formData
    formData.append('ItemName', $('#ItemName').val());
    formData.append('price', $('#Price').val());
    formData.append('quantity', $('#quantity').val());
    formData.append('description', $('#description').val());
    formData.append('outOfStock', $('#outOfStock').is(':checked'));

    // ...

    $.ajax({
        url: '/addItem',  // Update with your server endpoint
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            alert('Item added successfully!');
        },
        error: function(error) {
            alert('Error adding item.');
        }
    });
}