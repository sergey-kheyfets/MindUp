const modalAdd = document.getElementById('modal-add');
const imageLoad = document.getElementById('group-image-upload');
const modalImageUpload = document.querySelector('.modal-view').querySelector('.custom-image-upload');

function openModal() {
    modalAdd.style.opacity = 1;
    modalAdd.style.pointerEvents = 'auto';
}

function closeModal() {
    modalAdd.style.opacity = 0;
    modalAdd.style.pointerEvents = 'none';
}

document.querySelector('.block.group.add').onclick = openModal;
modalAdd.querySelector('.modal-blackout').onclick = closeModal;

imageLoad.addEventListener('change', () => {
    const image = imageLoad.files[0];
    if (image) {
        const reader = new FileReader();
        reader.onload = (e) => {
            modalImageUpload.style.backgroundImage = `url(${e.target.result})`;
        }
        reader.readAsDataURL(image);
    }
});

setGrid();