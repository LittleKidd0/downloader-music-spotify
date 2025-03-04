import fs from 'fs';
import axios from 'axios';


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

const url = 'https://spotisongdownloader.to/api/composer/spotify/wertyuht9847635.php';
const cookieHeader = await getCookies('https://spotisongdownloader.to');
const headers = {
    'Host': 'spotisongdownloader.to',
    'Cookie': cookieHeader,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://spotisongdownloader.to/playlist.php',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://spotisongdownloader.to',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Dnt': '1',
    'Sec-Gpc': '1',
    'Priority': 'u=0',
    'Te': 'trailers'
};

fs.readFile('data.json', 'utf8', async (err, data) => {
    if (err) {
        console.error('Error al leer el archivo:', err);
        return;
    }
    
    try {
        const jsonData = JSON.parse(data);
        const trackDetails = jsonData.track_details;
        let tracks = [];

        Object.keys(trackDetails).forEach(key => {
            if (!isNaN(key)) {
                const track = trackDetails[key];
                tracks.push({
                    link: track.link,
                    song_name: track.song_name,
                    artist: track.artist
                });
            }
        });

        fs.writeFile('datos3.json', JSON.stringify(tracks, null, 2), async (err) => {
            if (err) {
                console.error('Error al escribir el archivo datos3.json:', err);
                return;
            }
            console.log('Archivo datos3.json creado con éxito.');
            
            const results = [];
            for (const track of tracks) {
                const params = new URLSearchParams();
                params.append('song_name', track.song_name);
                params.append('artist_name', track.artist);
                params.append('url', track.link);

                try {
                    const response = await axios.post(url, params, { headers });
                    const dlink = response.data.dlink;
                    results.push(dlink);
                } catch (error) {
                    console.error(`Error al obtener dlink para ${track.song_name}:`, error);
                }
            }
            
            fs.writeFile('final.json', JSON.stringify(results, null, 2), (err) => {
                if (err) {
                    console.error('Error al escribir el archivo final.json:', err);
                    return;
                }
                console.log('Archivo final.json creado con éxito.');
            });
        });
    } catch (error) {
        console.error('Error al procesar el JSON:', error);
    }
});
