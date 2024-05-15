const nameEl = document.getElementById('profileName');
const emailEl = document.getElementById('profileEmail');
const pubDateEl = document.getElementById('profilePubDate');

async function updateProfile() {
    const meResult = await sendRequest('api/me');
    nameEl.textContent = `${meResult['name']} ${meResult['sur_name']} ${meResult['last_name']}`;
    emailEl.textContent = `Email: ${meResult['email']}`;
    pubDateEl.textContent = `Зарегистрирован: ${meResult['pub_date']}`;
}

updateProfile();
