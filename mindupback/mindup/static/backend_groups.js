async function getGroups() {
    const resp = await sendRequest('/mindup/api/all_groups');
    return resp.result;
}

function createGroupHTML(groupJson) {
    const groupId = groupJson['id'];
    const author = groupJson['creator'];
    const title = groupJson['title'];
    const description = groupJson['description'];
    const icon = groupJson['icon'];

    const blockElement = document.createElement('div');
    blockElement.classList.add('block');
    blockElement.onclick = () => { window.location.href = `meetings.html?group=${groupId}&title=${title}` };

    const blockBackgroundElement = document.createElement('div');
    blockBackgroundElement.classList.add('block-background');
    if (icon !== '-') {
        blockBackgroundElement.style.backgroundImage = `url('${icon}')`;
    }


    const h2Element = document.createElement('h2');
    h2Element.innerHTML = title;

    blockElement.appendChild(blockBackgroundElement);
    blockElement.appendChild(h2Element);

    return blockElement;
}

async function updateGroups() {
    const result = await getGroups();
    const blocks = document.querySelector('.blocks');
    for (const group of result) {
        const groupHTML = createGroupHTML(group);
        blocks.appendChild(groupHTML);
    }
    setGrid();
}

updateGroups();
