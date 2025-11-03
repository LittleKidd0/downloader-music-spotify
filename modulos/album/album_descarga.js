import fs from 'fs';
import axios from 'axios';
import qs from 'qs';
import path from "path";
import { fileURLToPath } from "url";

// ===== Reemplazo de __dirname en ES Modules =====
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ===== Leer PHPSESSID desde JSON (dentro de modulos/) =====
const phpsessidPath = path.join(__dirname, 'phpsessid.json');

let phpsessidObj;
try {
  phpsessidObj = JSON.parse(fs.readFileSync(phpsessidPath, 'utf8'));
} catch (err) {
  console.error('Error leyendo phpsessid.json:', err.message);
  process.exit(1);
}

const phpsessid = phpsessidObj.PHPSESSID;
console.log('PHPSESSID cargado:', phpsessid);

// ===== Funciones =====
async function getCookies(url) {
  try {
    const response = await axios.get(url, { withCredentials: true });
    let cookies = (response.headers['set-cookie'] || []).appString();
    cookies = cookies.replace(/PHPSESSID=[^;]+;?/g, '');
    const phpSessionMatch = response.headers['set-cookie'].appString().match(/PHPSESSID=([^;]+)/);
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
    url: track.url,
    zip_download: "false",
    quality: 'm4a',
  };

const headers = {
  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
  "Cookie": "_ga=; PHPSESSID=2tyECekSHks9Hp9CbBtEVRm2sMq0FKEB; quality=m4a",
  "Accept": "application/json, text/javascript, */*; q=0.01",
  "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
  "Accept-Encoding": "gzip, deflate, br",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
  "X-Requested-With": "XMLHttpRequest",
  "Referer": "https://spotisongdownloader.app/album.php",
  "Content-Length": "149",
  "Origin": "https://spotisongdownloader.app",
  "Sec-Fetch-Dest": "empty",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Site": "same-origin",
  "Priority": "u=0",
  "Te": "trailers"
};
  try {
    const response = await axios.post(
      'https://spotisongdownloader.app/api/composer/spotify/ssdw23456ytrfds.php',
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

// ===== Procesar tracks =====
async function processTracks() {
  try {
    const dataPath = path.join(__dirname, '../datos2.json'); // data en carpeta padre
    const data = fs.readFileSync(dataPath, 'utf8');
    const jsonData = JSON.parse(data);

    const cookieHeader = await getCookies('https://spotisongdownloader.app');

    const finalData = [];

    for (let index = 0; index < jsonData.track_details.length; index++) {
      const track = jsonData.track_details[index];
      const result = await downloadTrack(track, index, cookieHeader);
      if (result) finalData.push(result);
    }

    if (finalData.length > 0) {
      finalData.sort((a, b) => a.index - b.index);
      const finalPath = path.join(__dirname, '../final.json');
      fs.writeFileSync(finalPath, JSON.stringify(finalData, null, 2));
      console.log('🎉 All links saved successfully in final.json');
    } else {
      console.log('⚠️ Download links could not be obtained.');
    }
  } catch (err) {
    console.error('❌ Error processing tracks:', err.message);
  }
}

// ===== Ejecutar =====
processTracks();
