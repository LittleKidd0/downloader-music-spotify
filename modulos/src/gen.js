// script.js
// Generador de PHPSESSID seguro (32 caracteres por defecto)
// Uso: node script.js [longitud]
// Ejemplo: node script.js       -> genera 32 chars
//          node script.js 16    -> genera 16 chars


import crypto from 'crypto';
const DEFAULT_LENGTH = 32;
const CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

// Rejection-sampling para evitar sesgo al mapear bytes -> índices
function secureRandomIndex(max) {
  if (max <= 0 || max > 256) throw new RangeError('max must be 1..256');
  const threshold = 256 - (256 % max); // valores >= threshold se descartan
  while (true) {
    const buf = crypto.randomBytes(1);
    const val = buf[0];
    if (val < threshold) return val % max;
    // si val >= threshold, volver a intentar
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

// CLI
const arg = process.argv[2];
const length = arg ? Number(arg) : DEFAULT_LENGTH;
try {
  const id = generatePHPSESSID(length);
  console.log(id);
} catch (err) {
  console.error('Error:', err.message);
  process.exit(1);
}
