function copyUrlToClipboard(uuid, firstName, lastName) {

    var textarea = document.createElement('textarea');
    textarea.textContent = base_url + '/register/' + uuid;
    document.body.appendChild(textarea);
    var selection = document.getSelection();
    var range = document.createRange();
    range.selectNode(textarea);
    selection.removeAllRanges();
    selection.addRange(range);
    document.execCommand('copy');
    selection.removeAllRanges();
    document.body.removeChild(textarea);
    alert('Ссылка на регистрацию пользователя ' + firstName + " " + lastName +
        " была скопирована в буфер обмена");
}