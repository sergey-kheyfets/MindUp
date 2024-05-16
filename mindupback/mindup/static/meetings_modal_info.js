const modalInfo = document.getElementById('modal-info');

const titleInfo = modalInfo.querySelector('h1');
const timeInfo = modalInfo.querySelector('.datetime-place-info .time');
const placeInfo = modalInfo.querySelector('.datetime-place-info .place');
const tagsInfo  = modalInfo.querySelector('.tags');
const descriptionInfo = modalInfo.querySelector('.description');
const membersInfo = modalInfo.querySelector('.members-info');
const membersWrapper = modalInfo.querySelector('.members-wrapper');
const groupInfo = modalInfo.querySelector('.groupNameInfo');


function setupMembers(members, adminId) {
    membersWrapper.innerHTML = '';
    for (const member of members) {
        const memberDiv = document.createElement('div');
        memberDiv.className = 'member';
        memberDiv.textContent = member;
        membersWrapper.appendChild(memberDiv);
    }
}

function setupTags(tags) {
    tagsInfo.innerHTML = '';
    for (const tag of tags) {
        const tagDiv = document.createElement('div');
        tagDiv.className = 'tag';
        tagDiv.textContent = tag;
        tagsInfo.appendChild(tagDiv);
    }
}

function getMemberCountSync(membersList, max, isLimited) {
    let maxStr = max.toString();
    if (!isLimited) {
        maxStr = 'Ꝏ';
    }
    const current = membersList.length;
    return `${current} / ${maxStr}`;
}

async function setUpModalInfo(meetId, groupId) {
    const resTask = await sendRequest(`/api/group/${groupId}/meeting/${meetId}`);
    const res = resTask.result;
    console.log(res)

    titleInfo.textContent = res['title'];
    timeInfo.textContent = 'Время: ' + res['event_time'];
    placeInfo.textContent = 'Место: ' + res['place_text'];
    descriptionInfo.textContent = 'Описание: ' + res['description'];
    groupInfo.textContent = 'Группа: ' + res['organization_dict']['title'];
    membersInfo.textContent = 'Участники: ' + getMemberCountSync(res['members'], res['max_members_number'], res['is_max_members_number_limited']);
    setupTags(res['tags'], );
    setupMembers(res['members']);
}


async function openModalInfo(meetId, groupId) {
    await setUpModalInfo(meetId, groupId);
    modalInfo.style.opacity = 1;
    modalInfo.style.pointerEvents = 'auto';
}

function closeModalInfo() {
    modalInfo.style.opacity = 0;
    modalInfo.style.pointerEvents = 'none';
}

modalInfo.querySelector('.modal-blackout').onclick = closeModalInfo;