import fs from 'fs';
import fetch from 'node-fetch';

const url = process.argv[2];

if (!url) {
    process.exit(1);
}

const apiUrl = `https://spotisongdownloader.app/api/composer/spotify/xsingle_track.php?url=${url}`;

const headers = {
    "Host": "spotisongdownloader.app",
    "Cookie": "PHPSESSID=2tyECekSHks9Hp9CbBtEVRm2sMq0FKEB; quality=m4a",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Accept-Language": "es-ES",
    "Referer": "https://spotisongdownloader.app/",
    "X-Requested-With": "XMLHttpRequest",
    "Dnt": "1",
    "Sec-Gpc": "1",
};


async function fetchData() {
    try {
        const response = await fetch(apiUrl, { method: 'GET', headers: headers });

        if (!response.ok) {
            throw new Error(`Request error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log(data.JSON)

        fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
        console.log("Data saved in data.json");
    } catch (error) {
        console.error('Error:', error.message);
    }
}

fetchData();
