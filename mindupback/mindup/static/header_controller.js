const searchInput = document.getElementById('searchInput');

function search() {
    const text = searchInput.value;
    if (text !== '') {
        window.location.href = `https://www.google.com/search?q=${text}`;
    }
}

function handleKeyPress(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        search();
    }
}