window.addEventListener('resize', () => {
    const block = document.querySelector('.block');
    // const blockWidth = Number(block.style.width);
    // console.log(block.style.width)
    const blockWidth = 400;
    const screenWidth = window.innerWidth;
    const colsCount = Math.floor(screenWidth * 0.9 / blockWidth);
    console.log(colsCount)
    const groups = document.querySelector('.groups');
    console.log(groups.style.gridTemplateColumns)
    groups.style.gridTemplateColumns = `repeat(${colsCount}, 1fr)`;
})