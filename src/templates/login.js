const url_root = 'http://185.189.14.105:80/';

function add_to_cookie(json) {
    document.cookie = "access_token=" + json.access_token + '; max-age=900';
    document.cookie = "refresh_token=" + json.refresh_token + '; max-age=1209600';
}

function Redirect(postfix) {
    window.location.replace(url_root + postfix);
}

login_form.onsubmit = async (e) => {
    e.preventDefault();
    let formData = new FormData(login_form);
    console.log(login_form);
    const response = await fetch('http://185.189.14.105/auth?grant_type=password' + '&' + 'username=' +
        formData.get('username') +
        '&' + 'password=' + formData.get('password'), {
        method: 'POST'
    });

    if (response.status === 200) {
        let json = await response.json();
        console.log(json)
        add_to_cookie(json);
        res = await get_url(url_root, json.access_token);
        if (res.status === 200) {

            let newVar = await res.json();
            console.log(newVar)
            Redirect(newVar.url)
        }

    } else {
        alert('Пользователь с такими данными не зарегестрирован')
    }
};