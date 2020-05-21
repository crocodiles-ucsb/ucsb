const add_catalog = async (data, catalog_type, value = null) => {
    url = base_url + '/admins/catalogs/' + catalog_type + '?' + 'data=' + data;
    if (data === "") {
        alert("Некорректно введены данные");
        return;
    }
    if (value != null) {
        if (value <= 0) {
            alert("Числовое значение должно быть больше либо равно нулю");
            return
        }
        url = url + '&' + 'value=' + value;
    }
    const response = await fetch(url,{
        method : 'post'
    });
    switch (response.status) {
        case 201:
            alert("Данные успешно добавлены");
            return;
        case 401:
            alert("Данные авториазации устарели, обновите страницу");
            return;
        case 400:
            alert("Такой элемент справочника уже существует");
            return;
    }
};
