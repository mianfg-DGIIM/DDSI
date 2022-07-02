// Enviar formulario a servidor
document.getElementById("form-submit").onclick = function () {
    // validación Bootstrap
    var forms = document.getElementsByClassName('needs-validation');
    var validation = Array.prototype.filter.call(forms, function(formEl) {
        formEl.addEventListener('submit', function(event) {
        event.preventDefault();
        event.stopPropagation();
            
        if (formEl.checkValidity()) {
            console.log("is valid");
            const form = $("#form");

            // recopilar URL de POST
            var url = form.attr("action");

            console.log("url:", url)

            // construir formData
            var formData = {};
            form.serializeArray().forEach(inputItem =>
                formData[inputItem['name']] = inputItem['value']);
            
            // petición POST
            post(url, formData, function(response) {
                if (response.success) {
                    // si ha sido un éxito en el servidor
                    if (response.data.category === "success") {
                        // redirigimos a la página que nos indica
                        window.location.replace(response.data.data.redirect);
                    } else {
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
        } else console.log("NOT valid");
        //form.classList.add('was-validated');
        }, false);
    });
}
