import fs from 'fs';


const dataFile = fs.readFileSync('data.json', 'utf8');

const playlist = JSON.parse(dataFile);

const trackArray = Object.values(playlist.track_details).filter(item => item.link);

const orderedTracks = trackArray.sort((a, b) => a.song_name.localeCompare(b.song_name));

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
fs.writeFile('datos2.json', JSON.stringify(result, null, 2), (err) => {
  if (err) {
    console.error('Error saving file:', err);
  } else {
    console.log('File datos2.json saved successfully');
  }
});
