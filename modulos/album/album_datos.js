import fs from 'fs';
import fetch from 'node-fetch';

const url = process.argv[2];

if (!url) {
    process.exit(1);
}

const url_ = `https://spotisongdownloader.app/api/composer/spotify/xalbum.php?url=${url}`;

fetch(url_, {
  method: 'GET',
  headers: {
    'Host': 'spotisongdownloader.app',
    'Cookie': 'zprg=2; g_state={"i_l":0}; dcount=3; uemail=; upass=; _ParseUID=null; current_timezone=null; PHPSESSID=null',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20221904 Firefox/134.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://spotisongdownloader.app/',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Priority': 'u=0',
    'Te': 'trailers'
  }
})
  .then(response => response.json())
  .then(data => {
    fs.writeFile('datos2.json', JSON.stringify(data, null, 2), (err) => {
      if (err) {
        console.error('Error guardando el archivo:', err);
      } else {
        console.log('Archivo datos2.json guardado con éxito!');
      }
    });
  })
  .catch(error => {
    console.error('Error en la solicitud:', error);
  });