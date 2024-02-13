$(document).ready(function () {
  // Init
  $("#predecir").hide();
  $(".image-section").hide();
  $(".loader").hide();
  $("#result").hide();

  // Upload Preview
  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#imagePreview").css(
          "background-image",
          "url(" + e.target.result + ")"
        );
        $("#imagePreview").hide();
        $("#imagePreview").fadeIn(650);
      };
      reader.readAsDataURL(input.files[0]);
    }
  }
  $("#imageUpload").change(function () {
    $("#predecir").show();
    $(".image-section").show();
    $("#btn-predict").show();
    $("#result").text("");
    $("#result").hide();
    if (this.files && this.files[0]) {
      const reader = new FileReader();
      reader.onload = function(e) {
        // Crear un elemento de imagen y establecer el origen en la vista previa del archivo
        const imagePreview = document.getElementById('imagePreview');
        imagePreview.innerHTML = '<img src="' + e.target.result + '" />';
      }
      // Leer el archivo como una URL de datos
      reader.readAsDataURL(this.files[0]);
    }
    readURL(this);
  });

  // Predict
  $("#btn-predict").click(function () {
    var form_data = new FormData($("#upload-file")[0]);

    // Show loading animation
    $(this).hide();
    $(".loader").show();

    // Make prediction by calling api /predict
    $.ajax({
      type: "POST",
      url: "/predict",
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        // Get and display the result
        $(".loader").hide();
        $("#result").fadeIn(600);
        $("#result").text(" Resultado:  " + data);
        console.log("Success!");
      },
    });
  });
});

// const form = document.getElementById('upload-file');

// // Agregar un event listener para el evento 'change' del input de tipo archivo
// form.addEventListener('change', function() {
//   // Verificar si se ha cargado al menos un archivo
//   if (this.file && this.file.length > 0) {
//     // Mostrar la otra sección
//     document.querySelector('.image-section').style.display = 'block';
//   }
// });
