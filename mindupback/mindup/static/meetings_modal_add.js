const modalAdd = document.getElementById('modal-add');


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
