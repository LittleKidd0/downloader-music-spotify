import fs from 'fs';
import crypto from 'crypto';
import path from "path";
import { fileURLToPath } from "url";

const DEFAULT_LENGTH = 32;
const CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

// Rejection-sampling para evitar sesgo al mapear bytes -> índices
function secureRandomIndex(max) {
  if (max <= 0 || max > 256) throw new RangeError('max must be 1..256');
  const threshold = 256 - (256 % max);
  while (true) {
    const buf = crypto.randomBytes(1);
    const val = buf[0];
    if (val < threshold) return val % max;
  }
}

function generatePHPSESSID(length = DEFAULT_LENGTH, charset = CHARSET) {
  if (!Number.isInteger(length) || length <= 0) {
    throw new TypeError('length must be a positive integer');
  }
  const chars = [];
  const m = charset.length;
  for (let i = 0; i < length; i++) {
    const idx = secureRandomIndex(m);
    chars.push(charset[idx]);
  }
  return chars.join('');
}

// --- Ruta del archivo JSON ---
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const jsonPath = path.join(__dirname, "phpsessid.json");

// --- Leer o crear phpsessid.json ---
let phpsessidObj;
if (fs.existsSync(jsonPath)) {
  try {
    phpsessidObj = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
  } catch (err) {
    console.error("Error parseando phpsessid.json, se generará uno nuevo:", err.message);
    phpsessidObj = { PHPSESSID: generatePHPSESSID() };
    fs.writeFileSync(jsonPath, JSON.stringify(phpsessidObj, null, 2));
  }
} else {
  phpsessidObj = { PHPSESSID: generatePHPSESSID() };
  fs.writeFileSync(jsonPath, JSON.stringify(phpsessidObj, null, 2));
}

const phpsessid = phpsessidObj.PHPSESSID;

// --- Usar el valor en tus peticiones ---
async function main() {
  // === PETICIÓN 1 ===
  await fetch("https://spotisongdownloader.app/", {
    method: "GET",
    headers: {
      "Host": "spotisongdownloader.app",
      "Cookie": `_ga=; PHPSESSID=${phpsessid}; quality=m4a; dcount=1`,
      "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding": "gzip, deflate, br",
      "Upgrade-Insecure-Requests": "1",
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "none",
      "Sec-Fetch-User": "?1",
      "Priority": "u=0, i",
      "Te": "trailers",
      "Connection": "keep-alive"
    }
  });

  // === PETICIÓN 2 ===
  await fetch("https://spotisongdownloader.app/ifCaptcha.php", {
    method: "GET",
    headers: {
      "Host": "spotisongdownloader.app",
      "Cookie": `_ga=; PHPSESSID=${phpsessid}; quality=m4a; dcount=1`,
      "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
      "Accept": "*/*",
      "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding": "gzip, deflate, br",
      "Referer": "https://spotisongdownloader.app/",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "Priority": "u=0",
      "Te": "trailers"
    }
  });

  // === PETICIÓN 3 ===
  const postData1 =
    "data=%255B%252220181002%2522%252C%25220m%25205s%2522%252C%2522https%253A%252F%252Fi.scdn.co%252Fimage%252Fab67616d0000b27340461e96808378ae2787a7e4%2522%252C%2522Mac%2520DeMarco%2522%252C%2522https%253A%252F%252Fopen.spotify.com%252Ftrack%252F4hVsTyDdaliuwc00bYrtsf%2522%252C%2522One%2520Wayne%2520G%2522%252C%25222023-04-21%2522%255D";

  await fetch("https://spotisongdownloader.app/track.php", {
    method: "POST",
    headers: {
      "Host": "spotisongdownloader.app",
      "Cookie": `_ga=; PHPSESSID=${phpsessid}; quality=m4a; dcount=1`,
      "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding": "gzip, deflate, br",
      "Referer": "https://spotisongdownloader.app/",
      "Content-Type": "application/x-www-form-urlencoded",
      "Content-Length": "333",
      "Origin": "https://spotisongdownloader.app",
      "Upgrade-Insecure-Requests": "1",
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "same-origin",
      "Sec-Fetch-User": "?1",
      "Priority": "u=0, i",
      "Te": "trailers"
    },
    body: postData1
  });

  // === PETICIÓN 4 ===
  const postData2 =
    "song_name=20181002&artist_name=Mac+Demarco&url=https%3A%2F%2Fopen.spotify.com%2Ftrack%2F4hVsTyDdaliuwc00bYrtsf&zip_download=false&quality=m4a";

  const response = await fetch("https://spotisongdownloader.app/api/composer/spotify/ssdw23456ytrfds.php", {
    method: "POST",
    headers: {
      "Host": "spotisongdownloader.app",
      "Cookie": `_ga=; PHPSESSID=${phpsessid}; quality=m4a; dcount=1`,
      "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
      "Accept": "application/json, text/javascript, */*; q=0.01",
      "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding": "gzip, deflate, br",
      "Referer": "https://spotisongdownloader.app/track.php",
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      "X-Requested-With": "XMLHttpRequest",
      "Content-Length": "141",
      "Origin": "https://spotisongdownloader.app",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "Priority": "u=0",
      "Te": "trailers"
    },
    body: postData2
  });
  console.log("Response Data:", await response.text());
  console.log("Status Code:", response.status);
}

// Ejecutar
main().catch(console.error);
// Este script es para dejar listo el PHPSESSID para hacer las descargas :p



