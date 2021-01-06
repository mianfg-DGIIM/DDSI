function deleteItem(table, id) {
    post('/api/'+table+'/delete/'+id, {}, function(response) {
        if (response.success) {
            if (response.data.category === "success") {
                window.location.replace(response.data.data.redirect);
            } else {
                console.log(response.data.message);
            }
        } else {
            console.log("Parece que hay un problema contactando con el servidor...");
        }
    });
}