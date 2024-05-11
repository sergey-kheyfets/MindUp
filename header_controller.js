const searchInput = document.getElementById('searchInput');

function search() {
    const text = searchInput.value;
    if (text !== '')
        alert(text);
}

function handleKeyPress(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        search();
    }
}