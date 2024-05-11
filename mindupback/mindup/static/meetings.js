const tagLimit = 35;

function tagSearching(element) {
    searchInput.value = element.textContent;
}

setGrid();

function sendRequest(url) {
    return fetch(url).then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Request failed');
    });
}

async function getMeetings() {
    const resp = await sendRequest('/mindup/api/all_meetings');
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

function createMeetingsHTML(groupJson) {
    const author = `${groupJson['creator_dict']['sur_name']} ${groupJson['creator_dict']['name']}`;
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
                        <p class="person_additional-info">1 курс, Свердловское музыкальное училище им. П. И. Чайковского</p>
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
    const result = await getMeetings();
    const blocks = document.querySelector('.blocks-wrapper .blocks');
    for (const meeting of result) {
        const meetingHTML = createMeetingsHTML(meeting);
        blocks.appendChild(meetingHTML);
    }
    setGrid();
}

updateMeetings();