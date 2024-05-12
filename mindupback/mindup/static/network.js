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