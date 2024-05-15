const tagLimit = 35;
const emailLimit = 20;
const blocksWrapper = document.querySelector('.blocks-wrapper');
const groupTitle = document.querySelector('.source-group-name');
const groupIdInput = document.getElementById('meetingAddOrgId');
const backgroundContainer = document.querySelector('.background-container');

async function getMeetings() {
    const resp = await sendRequest('/mindup/api/all_meetings');
    return resp.result;
}

async function getGroupMeetings(groupId) {
    const resp = await sendRequest(`api/group/${groupId}/meetings`);
    return resp.result;
}

async function getBackgroundImageUrl(groupId) {
    const resp = await sendRequest('/mindup/api/all_groups');
    for (const group of resp.result) {
        if (group['id'] == groupId) {
            return group['icon'];
        }
    }
    return '-';
}

async function setBackgroundImage(groupId) {
    const url = await getBackgroundImageUrl(groupId);
    if (url !== '-') {
        backgroundContainer.style.backgroundImage = `url("${url}")`;
    } else {
        backgroundContainer.style.backgroundImage = 'url("site_images/background_blured.png")';
    }
}

function createTagsWrapper(tags) {
    const tagsWrapper = document.createElement('div');
    tagsWrapper.classList.add('tags-wrapper');

    const tagsHTML = document.createElement('div');
    tagsHTML.classList.add('tags');

    let totalLength = 0;

    for (const tag of tags) {
        const tagHTML = document.createElement('div');
        tagHTML.classList.add('tag');
        tagHTML.textContent = tag;
        totalLength += tag.length;
        if (totalLength >= tagLimit) {
            const button = document.createElement('button');
            button.textContent = 'посмотреть все';
            tagsWrapper.appendChild(tagsHTML);
            tagsWrapper.appendChild(button);
            break;
        } else {
            tagsHTML.appendChild(tagHTML);
        }
    }

    if (totalLength < tagLimit) tagsWrapper.appendChild(tagsHTML);

    return tagsWrapper;
}

function rightZeroFormat(value) {
    const strValue = value.toString();
    if (strValue.length === 1) {
        return '0' + strValue;
    }
    return strValue;
}

function getDateTime(eventTime) {
    const time = `${rightZeroFormat(eventTime.getHours())}:${rightZeroFormat(eventTime.getMinutes())}`;
    const year = eventTime.getFullYear().toString().substring(2,4);
    let month = rightZeroFormat(eventTime.getMonth() + 1);
    const date = `${rightZeroFormat(eventTime.getDate())}.${month}.${year}`;
    return [time, date];
}

function shortAuthorEmail(email) {
    if (email.length > emailLimit) {
        return 'Email: ' + email.slice(0, emailLimit - 3) + '...';
    }
    return 'Email: ' + email;
}

function renderMeetingStatusHTML(isMember, groupId, meetingId) {
    if (isMember) {
        const url = `/api/group/${groupId}/${meetingId}/unsignup`;
        const func = `fetch('${url}').then(() => location.reload())`;
        return `<img src="site_images/person_cancel.svg" alt="Отказаться" class="meeting-status" onclick="${func}">
                <div class="meeting-status-tooltip">Отказаться</div>`;
    } else {
        const url = `/api/group/${groupId}/${meetingId}/signup`;
        const func = `fetch('${url}').then(() => location.reload())`;
        return `<img src="site_images/person_ok.svg" alt="Записаться" class="meeting-status" onclick="${func}">
                <div class="meeting-status-tooltip">Записаться</div>`;
    }
}

function createMeetingsHTML(meetingJson) {
    const author = `${meetingJson['creator_dict']['sur_name']} ${meetingJson['creator_dict']['name']}`;
    const authorEmail = meetingJson['creator_dict']['email'];
    const title = meetingJson['title'];
    const groupId = meetingJson['organization_id'];
    const meetingId = meetingJson['meeting_id']
    const description = meetingJson['description'];
    const placeText = meetingJson['place_text'];
    const eventTime = new Date(meetingJson['event_time']);
    const [time, date] = getDateTime(eventTime);
    const tags = meetingJson['tags']
    const isMember = meetingJson['is_me_member']

    const block = `
        <div class="block">
            ${ renderMeetingStatusHTML(isMember, groupId, meetingId) }
            <div class="block-content">
                <div class="block-title-wrapper">
                    <div class="block-title">${title}</div>
                </div>
                <div class="block-info">
                    <div class="meeting-info-container">
                        <div class="icon-text-container">
                            <div class="datetime-wrapper">
                                <img src="site_images/time_medium.svg" alt="time icon">
                                <div class="datetime">
                                    <p class="date">${date}</p>
                                    <p class="time">${time}</p>
                                </div>
                            </div>
                            <div class="place-wrapper">
                                <img src="site_images/place.svg" alt="place icon">
                                <p>${placeText}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="person-container">
                    <img src="site_images/person.svg" alt="person icon">
                    <div class="person-info">
                        <p class="person-name">${author}</p>
                        <p class="person-additional-info" title="${authorEmail}">${shortAuthorEmail(authorEmail)}</p>
                    </div>
                </div>
            </div>
        </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = block;

    const blockInfo = div.querySelector('.block-info');
    const tagsWrapper = createTagsWrapper(tags);
    blockInfo.appendChild(tagsWrapper);

    return div;
}

async function updateMeetings() {
    const groupId = getUrlParameter('group');
    const backgroundTask = setBackgroundImage(groupId);
    let resultTask;
    if (groupId === null) {
        resultTask = getMeetings();
    } else {
        groupIdInput.value = groupId;
        resultTask = getGroupMeetings(groupId);
        const groupName = getUrlParameter('title');
        if (groupName !== null) {
            blocksWrapper.style.paddingTop = 0;
            groupTitle.textContent = groupName;
            groupTitle.style.display = 'block';
        }
    }
    const [result, _] = await Promise.all([resultTask, backgroundTask])

    const blocks = document.querySelector('.blocks-wrapper .blocks');
    for (const meeting of result) {
        const meetingHTML = createMeetingsHTML(meeting);
        blocks.appendChild(meetingHTML);
    }
    setGrid();
}

updateMeetings();