import fs from 'fs';
import axios from 'axios';
import qs from 'qs';

const dataFile = fs.readFileSync('data.json', 'utf8');

const jsonData = JSON.parse(dataFile);

const url = "https://spotisongdownloader.to/api/composer/spotify/wertyuht3456.php";

const song_name2 = jsonData.song_name;
const artist2 = jsonData.artist;
const url2 = jsonData.url;

const formData = {
  song_name: song_name2,
  artist_name: artist2,
  url: url2
};

const headers = {
  'Host': 'spotisongdownloader.to',
  'Cookie': 'PHPSESSID=m6tt49a1bn65dllk3o99p6455v; quality=m4a',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20221904 Firefox/134.0',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
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

axios.post(url, qs.stringify(formData), { headers })
  .then(response => {
    if (response.status === 200) {
      console.log("Data successfully obtained!");

      const dlink = response.data.dlink;

      let finalData = {};
      if (fs.existsSync('final.json')) {
        const finalFile = fs.readFileSync('final.json', 'utf8');
        finalData = JSON.parse(finalFile);
      }

      finalData.dlink = dlink;

      fs.writeFileSync('final.json', JSON.stringify(finalData, null, 2));

    } else {
      console.log(`Error: ${response.status}`);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
