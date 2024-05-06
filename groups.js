window.addEventListener('resize', () => {
    const block = document.querySelector('.block');
    // const blockWidth = Number(block.style.width);
    // console.log(block.style.width)
    const blockWidth = 400;
    const screenWidth = window.innerWidth;
    let colsCount = Math.floor(screenWidth * 0.9 / blockWidth);
    colsCount = Math.max(colsCount, 1);
    const groups = document.querySelector('.groups-wrapper .groups');
    groups.style.gridTemplateColumns = `repeat(${colsCount}, 1fr)`;
})