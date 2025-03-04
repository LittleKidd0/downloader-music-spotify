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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.1) AppleWebKit/619.36 (KHTML, like Gecko) Version/15.3.90 Safari/619.36',
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
        console.error('Error reading file:', err);
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
                console.error('Error writing file datos3.json:', err);
                return;
            }
            console.log('File datos3.json created successfully.');
            
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
                    console.error(`Error getting dlink for ${track.song_name}:`, error);
                }
            }
            
            fs.writeFile('final.json', JSON.stringify(results, null, 2), (err) => {
                if (err) {
                    console.error('Error writing final.json file:', err);
                    return;
                }
                console.log('Final.json file created successfully.');
            });
        });
    } catch (error) {
        console.error('Error processing JSON:', error);
    }
});
