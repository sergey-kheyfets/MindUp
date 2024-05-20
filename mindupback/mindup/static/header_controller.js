const searchInput = document.getElementById('searchInput');
const profileInfo = document.querySelector('.profile-info-container');
let isProfileOpened = false;

function search() {
    const text = searchInput.value;
    if (text !== '') {
        window.location.href = `https://www.google.com/search?q=${text}`;
    }
}

function closeProfileInfo() {
    profileInfo.style.opacity = 0;
    profileInfo.style.pointerEvents = 'none';
    isProfileOpened = false;
}

function openProfileInfo() {
    if (isProfileOpened) {
        closeProfileInfo();
    } else {
        profileInfo.style.opacity = 1;
        profileInfo.style.pointerEvents = 'auto';
        isProfileOpened = true;
    }
}

document.addEventListener('click', function(event) {
    if (!profileInfo.contains(event.target) && !event.target.closest('.menuGroup.profile')) {
        closeProfileInfo();
    }
});
