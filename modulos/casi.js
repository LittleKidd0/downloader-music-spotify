import fs from 'fs';
import axios from 'axios';
import qs from 'qs';

const url = 'https://spotisongdownloader.to/api/composer/spotify/wertyuht9847635.php';

let jsonData;
try {
  const dataFile = fs.readFileSync('data.json', 'utf8');
  jsonData = JSON.parse(dataFile);
} catch (error) {
  console.error('Error reading or parsing data.json:', error.message);
  process.exit(1);
}

const song_name2 = jsonData.song_name;
const artist2 = jsonData.artist;
const url2 = jsonData.url;

async function getCookies(url) {
  try {
    const response = await axios.get(url, { withCredentials: true });
    let cookies = (response.headers['set-cookie'] || []).toString();
    cookies = cookies.replace(/PHPSESSID=[^;]+;?/g, '');
    const phpSessionMatch = response.headers['set-cookie'].toString().match(/PHPSESSID=([^;]+)/);
    const phpSessionID = phpSessionMatch ? `PHPSESSID=${phpSessionMatch[1]}` : '';
    return `${phpSessionID}; quality=m4a`;
  } catch (error) {
    console.error('Error obtaining cookies:', error.message);
    return '';
  }
}

async function downloadSong() {
  try {
    const cookieHeader = await getCookies('https://spotisongdownloader.to');

    const headers = {
      'Host': 'spotisongdownloader.to',
      'Cookie': cookieHeader,
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.1; rv:133.0) Gecko/20110101 Firefox/133.0',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate, br',
      'Referer': 'https://spotisongdownloader.to/track.php',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'X-Requested-With': 'XMLHttpRequest',
      'Origin': 'https://spotisongdownloader.to',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Ch-Ua-Platform': 'macOS',
      'Sec-Ch-Ua-Mobile': '?0',
      'Dnt': '1',
      'Sec-Gpc': '1',
      'Priority': 'u=0',
      'Te': 'trailers'
    };

    const formData = {
      song_name: song_name2,
      artist_name: artist2,
      url: url2
    };

    const response = await axios.post(url, qs.stringify(formData), { headers });
    if (response.status === 200) {
      fs.writeFileSync('final.json', JSON.stringify(response.data, null, 2));
    } else {
      console.error(`Response error: ${response.status}`);
    }
  } catch (error) {
    console.error('Error obtaining data:', error.message);
  }
}

downloadSong();
