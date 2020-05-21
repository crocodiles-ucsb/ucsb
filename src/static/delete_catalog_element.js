delete_catalog_element = async (catalog_id) => {
    url = base_url + "/admins/catalogs/" + catalog_id;
    response = await fetch(url, {
        method: 'delete',
    });
    switch (response.status) {
        case 204:
            window.location = base_url;
            return;
        case 401:
            alert("Данные авторизации устарели, обновите страницу");
            return;
        case 404:
            alert("Элемент не найден, обновите страницу")
    }
}