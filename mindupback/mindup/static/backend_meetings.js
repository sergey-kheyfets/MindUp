const tagLimit = 35;
const emailLimit = 20;
const blocksWrapper = document.querySelector('.blocks-wrapper');
const groupTitle = document.querySelector('.source-group-name');
const groupIdInput = document.getElementById('meetingAddOrgId');

async function getMeetings() {
    const resp = await sendRequest('/mindup/api/all_meetings');
    return resp.result;
}

async function getGroupMeetings(groupId) {
    const resp = await sendRequest(`api/group/${groupId}/meetings`);
    return resp.result;
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

function getDateTime(eventTime) {
    const time = `${eventTime.getHours()}:${eventTime.getMinutes()}`;
    const year = eventTime.getFullYear().toString().substring(2,4)
    let month = (eventTime.getMonth() + 1).toString();
    if (month.length === 1) {
        month = '0' + month;
    }
    const date = `${eventTime.getDate()}.${month}.${year}`;
    return [time, date];
}

function shortAuthorEmail(email) {
    if (email.length > emailLimit) {
        return 'Email: ' + email.slice(0, emailLimit - 3) + '...';
    }
    return 'Email: ' + email;
}

function createMeetingsHTML(groupJson) {
    const author = `${groupJson['creator_dict']['sur_name']} ${groupJson['creator_dict']['name']}`;
    const authorEmail = groupJson['creator_dict']['email'];
    const title = groupJson['title'];
    const description = groupJson['description'];
    const placeText = groupJson['place_text'];
    const eventTime = new Date(groupJson['event_time']);
    const [time, date] = getDateTime(eventTime);
    const tags = groupJson['tags']
    const isMember = groupJson['is_me_member']

    const block = `
        <div class="block">
            <img src="site_images/person_cancel.svg" alt="Отказаться" class="meeting-status">
            <div class="meeting-status-tooltip">Отказаться</div>
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
    let result;
    if (groupId === null) {
        result = await getMeetings();
    } else {
        const groupName = getUrlParameter('title');
        groupIdInput.value = groupId;
        result = await getGroupMeetings(groupId);
        blocksWrapper.style.paddingTop = 0;
        groupTitle.textContent = groupName;
        groupTitle.style.display = 'block';
    }

    const blocks = document.querySelector('.blocks-wrapper .blocks');
    for (const meeting of result) {
        const meetingHTML = createMeetingsHTML(meeting);
        blocks.appendChild(meetingHTML);
    }
    setGrid();
}

updateMeetings();