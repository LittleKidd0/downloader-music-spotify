import fs from 'fs'; // Para manejar archivos

// Datos proporcionados


const dataFile = fs.readFileSync('data.json', 'utf8');

const playlist = JSON.parse(dataFile);

// Convertir el objeto `track_details` en un array para poder ordenar
const trackArray = Object.values(playlist.track_details).filter(item => item.link); // Filtramos solo las canciones

// Ordenar las canciones por nombre (puedes cambiar esto por otro criterio si lo prefieres)
const orderedTracks = trackArray.sort((a, b) => a.song_name.localeCompare(b.song_name));

// Crear el objeto con el formato solicitado
const result = {
  actual_count: playlist.track_details.actual_count,
  count: playlist.track_details.count,
  aname: playlist.track_details.pname,
  artist: playlist.track_details.artist || 'Desconocido',
  img: playlist.track_details.pimg,
  released: playlist.track_details.released || 'Desconocido',
  track_details: orderedTracks.map(track => ({
    artist: track.artist,
    name: track.song_name,
    time: track.duration,
    url: track.link
  }))
};

// Guardar en un archivo JSON llamado "datos2.json"
fs.writeFile('datos2.json', JSON.stringify(result, null, 2), (err) => {
  if (err) {
    console.error('Error al guardar el archivo:', err);
  } else {
    console.log('Archivo datos2.json guardado con éxito');
  }
});
