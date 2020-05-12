function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}


async function get_url(url, token) {
    return (await fetch(url, {
        headers: new Headers({
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    }));
}

const url_root = 'http://185.189.14.105/';

function Redirect(postfix) {
    window.location.replace(url_root + postfix);
}

const f = (response) => {
    if (response.status === 200) {
        response.json().then((json) => Redirect(json.url))
    } else {
        console.log('error')
    }

};
const url = url_root + 'role';
// document.cookie = 'access_token=123; max-age=900';
let access_token = 'access_token';
if (document.cookie.includes(access_token)) {
    let cookie = getCookie(access_token);
    if (cookie) {
        get_url(url + 'role', cookie)
            .then(f)
    }
} else {
    Redirect('login')
}