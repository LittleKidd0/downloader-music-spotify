import fs from 'fs';
import axios from 'axios';
import qs from 'qs';

async function getCookies(url) {
  try {
    const response = await axios.get(url, { withCredentials: true });
    let cookies = (response.headers['set-cookie'] || []).toString();
    cookies = cookies.replace(/PHPSESSID=[^;]+;?/g, '');
    const phpSessionMatch = response.headers['set-cookie'].toString().match(/PHPSESSID=([^;]+)/);
    const phpSessionID = phpSessionMatch ? `PHPSESSID=${phpSessionMatch[1]}` : '';
    return `${phpSessionID}; quality=m4a`;
  } catch (error) {
    console.error('❌ Error obtaining cookies:', error.message);
    return '';
  }
}

async function downloadTrack(track, index, cookieHeader) {
  const formData = {
    song_name: track.name,
    artist_name: track.artist,
    url: track.url
  };

  const headers = {
    'Host': 'spotisongdownloader.to',
    'Cookie': `${cookieHeader}; _ga=; quality=m4a`,
    'User-Agent': 'Linux_Parrot/_LittleKidd0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://spotisongdownloader.to/album.php',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://spotisongdownloader.to',
    'Dnt': '1',
    'Sec-Gpc': '1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Priority': 'u=0',
    'Te': 'trailers'
  };

  try {
    const response = await axios.post(
      'https://spotisongdownloader.to/api/composer/spotify/ssdw23456ytrfds.php',
      qs.stringify(formData),
      { headers }
    );

    if (response.status === 200) {
      console.log(`✅ Track ${index + 1}: ${track.name} - ${track.artist} | Download link obtained`);
      return {
        index: index + 1,
        song: track.name,
        artist: track.artist,
        downloadLink: response.data.dlink
      };
    } else {
      console.error(`❌ Error in response: ${response.status}`);
      return null;
    }
  } catch (error) {
    console.error(`❌ Error downloading track "${track.name}":`, error.message);
    return null;
  }
}

async function processTracks() {
  try {
    const data = fs.readFileSync('datos2.json', 'utf8');
    const jsonData = JSON.parse(data);
    const cookieHeader = await getCookies('https://spotisongdownloader.to');

    const finalData = [];

    for (let index = 0; index < jsonData.track_details.length; index++) {
      const track = jsonData.track_details[index];
      const result = await downloadTrack(track, index, cookieHeader);
      if (result) finalData.push(result);
    }

    if (finalData.length > 0) {
      finalData.sort((a, b) => a.index - b.index);
      fs.writeFileSync('final.json', JSON.stringify(finalData, null, 2));
      console.log('🎉 All links saved successfully in final.json');
    } else {
      console.log('⚠️ Download links could not be obtained.');
    }
  } catch (err) {
    console.error('❌ Error processing tracks:', err.message);
  }
}

processTracks();
