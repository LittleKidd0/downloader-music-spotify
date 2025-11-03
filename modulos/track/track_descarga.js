// modulos/casi.js
import fs from 'fs';
import axios from 'axios';
import qs from 'qs';
import path from "path";
import { fileURLToPath } from "url";

// ===== Reemplazo de __dirname en ES Modules =====
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ===== Leer PHPSESSID desde JSON (dentro de modulos/) =====
const jsonPath = path.join(__dirname, 'phpsessid.json');

let phpsessidObj;
try {
  phpsessidObj = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
} catch (err) {
  console.error('Error leyendo phpsessid.json:', err.message);
  process.exit(1);
}

const phpsessid = phpsessidObj.PHPSESSID;

// ===== Leer data.json (afuera de modulos/) =====
const dataJsonPath = path.join(__dirname, '../data.json');
let jsonData;
try {
  jsonData = JSON.parse(fs.readFileSync(dataJsonPath, 'utf8'));
} catch (error) {
  console.error('Error leyendo data.json:', error.message);
  process.exit(1);
}

const { song_name: song_name2, artist: artist2, url: url2 } = jsonData;
console.log(jsonData)

// ===== Función principal =====
async function downloadSong() {
  try {
    const headers = {
      'Host': 'spotisongdownloader.app',
      'Cookie': `PHPSESSID=4ecce4dd3ab80d12b7e9fc8134e66b31; _ga=; quality=m4a`,
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.1; rv:133.0) Gecko/20110101 Firefox/133.0',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate, br',
      'Referer': 'https://spotisongdownloader.app/track.php',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'X-Requested-With': 'XMLHttpRequest',
      'Origin': 'https://spotisongdownloader.app',
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
      url: url2,
      zip_download: false,
      quality: "m4a"
    };
    console.log(formData)

    const url = 'https://spotisongdownloader.app/api/composer/spotify/ssdw23456ytrfds.php';
    const response = await axios.post(url, qs.stringify(formData), { headers });

    if (response.status === 200) {
      // Guardar final.json afuera de modulos/
      const finalPath = path.join(__dirname, '../final.json');
      fs.writeFileSync(finalPath, JSON.stringify(response.data, null, 2));
      console.log("Datos guardados en final.json ✅");
    } else {
      console.error(`Error en la respuesta: ${response.status}`);
    }
  } catch (error) {
    console.error('Error obteniendo datos:', error.message);
  }
}

// ===== Ejecutar =====
downloadSong();