function setGrid() {
    const blocks = document.querySelector('.blocks').querySelectorAll('.block');
    const title = document.querySelector('title').textContent;
    let blockWidth = 300;
    if (title === 'Встречи') {
        blockWidth = 340;
    }
    const screenWidth = window.innerWidth;
    let colsCount = Math.floor(screenWidth * 0.9 / blockWidth);
    colsCount = Math.min(colsCount, blocks.length);
    colsCount = Math.max(colsCount, 1);
    const groups = document.querySelector('.blocks');
    groups.style.gridTemplateColumns = `repeat(${colsCount}, 1fr)`;
}

window.addEventListener('resize', setGrid);
