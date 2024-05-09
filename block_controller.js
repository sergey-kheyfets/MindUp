function setGrid() {
    const blocks = document.querySelector('.blocks').querySelectorAll('.block');
    const blockWidth = 300;
    const screenWidth = window.innerWidth;
    let colsCount = Math.floor(screenWidth * 0.9 / blockWidth);
    colsCount = Math.min(colsCount, blocks.length);
    colsCount = Math.max(colsCount, 1);
    const groups = document.querySelector('.blocks');
    groups.style.gridTemplateColumns = `repeat(${colsCount}, 1fr)`;
}

window.addEventListener('resize', setGrid);
