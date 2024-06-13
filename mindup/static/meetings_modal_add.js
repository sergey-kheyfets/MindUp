const modalAdd = document.getElementById('modal-add');
const tagsWrapper = modalAdd.querySelector('.tags');
const tagsAddHint = tagsWrapper.querySelector('.tags-add-hint');
const addTagButton = document.getElementById('addTag');

const limitCheckbox = document.getElementById('max_members_number_input');
const numberInput = document.getElementById('member_limit');

let tagsCount = 0;


function reloadForm() {
    tagsAddHint.style.opacity = 1;
    tagsAddHint.style.display = 'block';
    tagsCount = 0;
    for (const tag of tagsWrapper.querySelectorAll('label')) {
        tag.remove();
    }
    limitCheckbox.checked = false;
    for (const inputEl of modalAdd.querySelectorAll('input')) {
        inputEl.value = '';
    }
    modalAdd.querySelector('textarea').value = '';
}


function openModal() {
    modalAdd.style.opacity = 1;
    modalAdd.style.pointerEvents = 'auto';
}

function closeModal() {
    modalAdd.style.opacity = 0;
    modalAdd.style.pointerEvents = 'none';
}

document.querySelector('.block.add').onclick = openModal;
modalAdd.querySelector('.modal-blackout').onclick = closeModal;



function createTagInput() {
    const label = document.createElement('label');
    const input = document.createElement('input');
    input.type = 'text';
    input.classList.add('tag');
    input.name = `tag${++tagsCount}`;
    input.required = true;
    let curWidth = 116;
    input.addEventListener('input', function() {
        const textWidth = input.scrollWidth;
        if (textWidth > curWidth) {
            curWidth = textWidth - 16;
            input.style.width = `${curWidth}px`;
        }
    });

    label.appendChild(input);
    return label;
}

function insertTagInput(label) {
    tagsWrapper.insertBefore(label, addTagButton);
}

function addTag() {
    if (tagsCount === 0) {
        tagsAddHint.style.opacity = 0;
        setTimeout(() => {tagsAddHint.style.display = 'none';}, 200)

    }
    const label = createTagInput();
    setTimeout(() => {insertTagInput(label);}, 200)
}

addTagButton.onclick = addTag;



limitCheckbox.addEventListener('change', function() {
    if (this.checked) {
        numberInput.disabled = false;
        numberInput.style.backgroundColor = "white";

    } else {
        numberInput.disabled = true;
        numberInput.style.backgroundColor = "#f1f1f1";
    }
});


