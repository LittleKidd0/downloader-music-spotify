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
    console.error('Error obtaining cookies:', error.message);
    return '';
  }
}

fs.readFile('datos2.json', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the song file:', err);
    return;
  }

  const jsonData = JSON.parse(data);
  const finalData = [];

  jsonData.track_details.forEach((track, index) => {
    console.log(`Track ${index + 1}:`);
    console.log('  Artist:', track.artist);
    console.log('  Song name:', track.name);
    console.log('  Duration:', track.time);
    console.log('  URL:', track.url);
    console.log('');

    const formData = {
      song_name: track.name,
      artist_name: track.artist,
      url: track.url
    };

    getCookies('https://spotisongdownloader.to').then(cookieHeader => {
      const headers = {
        'Host': 'spotisongdownloader.to',
        'Cookie': cookieHeader,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20221904 Firefox/134.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://spotisongdownloader.to/track.php',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://spotisongdownloader.to',
        'Dnt': '1',
        'Sec-Gpc': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Priority': 'u=0',
        'Te': 'trailers'
      };

      axios.post("https://spotisongdownloader.to/api/composer/spotify/wertyuht3456.php", qs.stringify(formData), { headers })
        .then(response => {
          if (response.status === 200) {
            console.log("Data successfully obtained!");

            const dlink = response.data.dlink;

            finalData.push({
              index: index + 1,
              song: track.name,
              artist: track.artist,
              downloadLink: dlink
            });

            if (finalData.length === jsonData.track_details.length) {
              finalData.sort((a, b) => a.index - b.index);
              fs.writeFileSync('final.json', JSON.stringify(finalData, null, 2));
              console.log("Data successfully saved to final.json");
            }
          } else {
            console.log(`Error: ${response.status}`);
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });
});
