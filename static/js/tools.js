// AJAX POST request
function post(url, data, handleResponse) {
    /*
    Cómo usar esta función
    ----------------------

    Valores pasados:
        - url: URL del endpoint para la petición POST
        - data: datos que serán enviados al servidor
        - handleResponse: handler para respuesta del servidor (ver abajo)

    AJAX es **asíncrono**, por lo que devolver valores que retorne
    la petición no es factible, por eso usamos handlers.

    Básicamente, para usar esta función haz:

    post(url, data, function(response) {
        // aquí puedes hacer uso de response.code y response.data:
        //  - response.success: true si success, false si error
        //  - response.data: datos retornados por la petición

        // un ejemplo de uso
        if (response.success)
            console.log("respuesta satisfactoria:", response.data);
        else
            console.log("error en respuesta:", response.data);
    });
    */

    $.post(url, {data: JSON.stringify(data)}).done(function(responseData) {
        // on server answer
        handleResponse({
            success:    true,
            data:       responseData
        });
    }).fail(function(responseData) {
        // on server fail
        handleResponse({
            success:    false,
            data:       responseData
        });
    });
}