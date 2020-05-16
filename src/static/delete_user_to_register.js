function delete_user_to_register(uuid) {
    fetch(base_url + "/users/" + uuid, {
        method: "delete"
    }).then((response) => {
        if (response.status === 204) {
            window.location = base_url
        } else {
            response.json().then((json) => {
                alert(json.detail)
            })

        }
    })
}