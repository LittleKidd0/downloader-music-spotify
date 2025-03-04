import fetch from 'node-fetch';
import fs from 'fs';

const url = process.argv[2];

if (!url) {
    process.exit(1);
}


const url_ = `https://spotisongdownloader.to/api/composer/spotify/xplaylist_info.php?url=${url}`;
console.log(url_)

const headers = {
    'Host': 'spotisongdownloader.to',
    'Cookie': 'PHPSESSID=LittleKidd0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.1) AppleWebKit/618.19 (KHTML, like Gecko) Version/16.1.31 Safari/618.19',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://spotisongdownloader.to/',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Dnt': '1',
    'Sec-Gpc': '1',
    'Priority': 'u=0',
    'Te': 'trailers',
};
async function getPlaylistData() {
    try {
        const response = await fetch(url_, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            throw new Error('Error getting data: ' + response.statusText);
        }
        const data = await response.json();

        fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
        console.log('Data stored in data.json');
    } catch (error) {
        console.error('There was an error:', error);
    }
}

getPlaylistData();
