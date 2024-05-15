const modalInfo = document.getElementById('modal-info');

const titleInfo = modalInfo.querySelector('h1');
const timeInfo = modalInfo.querySelector('.datetime-place-info .time');
const placeInfo = modalInfo.querySelector('.datetime-place-info .place');
const tagsInfo  = modalInfo.querySelector('.tags');
const descriptionInfo = modalInfo.querySelector('.description');
const membersInfo = modalInfo.querySelector('.members-info');
const membersWrapper = modalInfo.querySelector('.members-wrapper');


function setupMembers(members) {
    for (const member of members) {
        const memberDiv = document.createElement('div');
        memberDiv.className = 'member';
        memberDiv.textContent = name;

        membersWrapper.appendChild(memberDiv);
    }
}

async function setUpModalInfo(meetId) {
    const res = sendRequest(``);
    
}


async function openModalInfo(meetId) {
    await setUpModalInfo(meetId);
    modalInfo.style.opacity = 1;
    modalInfo.style.pointerEvents = 'auto';
}

function closeModalInfo() {
    modalInfo.style.opacity = 0;
    modalInfo.style.pointerEvents = 'none';
}

modalInfo.querySelector('.modal-blackout').onclick = closeModalInfo;