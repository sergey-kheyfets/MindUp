const GENERAL_GROUP_ID = 17;


function sendRequest(url) {
    return fetch(url).then(response => {
        if (response.ok) {
            return response.json();
        } else if (response.status >= 500) {
            alert('Войдите в аккаунт еще раз');
            window.location.href = '/authorisation.html'
        }
        throw new Error('Request failed');
    });
}

function getUrlParameter(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function checkAuthorization() {
    if (document.cookie.split(';').length < 2) {
        window.location.href = '/';
    }
}
