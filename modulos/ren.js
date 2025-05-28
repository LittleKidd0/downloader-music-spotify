import fs from'fs';
import path from'path';

const outputFolder = 'result';


fs.readdir(outputFolder, (err, files) => {
    if (err) {
        console.error('Error reading folder:', err);
        return;
    }

   
    files.forEach(file => {
        if (file.includes("phmp3?fname=")) {
            const newFileName = file.replace("phmp3?fname=", "");
            const oldPath = path.join(outputFolder, file);
            const newPath = path.join(outputFolder, newFileName);

            
            fs.rename(oldPath, newPath, (err) => {
            });
        }
    });
});
