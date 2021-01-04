// Validación de formularios en Bootstrap
(function() {
    'use strict';
    window.addEventListener('load', function() {
    var forms = document.getElementsByClassName('needs-validation');
    var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
        }, false);
    });
    }, false);
})();

// Enviar formulario a servidor
document.getElementById("form-submit").onclick = function () {
    const form = $("#form");

    // recopilar URL de POST
    var url = form.attr("action");

    // construir formData
    var formData = {};
    form.serializeArray().forEach(inputItem =>
        formData[inputItem['name']] = inputItem['value']);
    
    // petición POST
    console.log("url:", url, "data:", formData);
    post(url, formData, function(response) {
        if (response.success) {
            // si ha sido un éxito en el servidor
            if (response.data.category === "success") {
                // redirigimos a la página que nos indica
                console.log("success: ", response)
                window.location.replace(response.data.data.redirect);
            } else {
                console.log("error: ", response)
                // modificamos el mensaje del cuadro de error
                $("#form-error-text").html(response.data.message);
                // mostramos el cuadro de error
                $("#form-error").attr("hidden", false);
            }            
        } else {
            // modificamos el mensaje del cuadro de error
            $("#form-error-text").html("Parece que hay un problema. Prueba a recargar la página e inténtalo de nuevo");
            // mostramos el cuadro de error
            $("#form-error").attr("hidden", false);
        }
    });
}