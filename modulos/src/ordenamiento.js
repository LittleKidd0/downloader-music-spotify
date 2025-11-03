import fs from 'fs';

fs.readFile('final.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading file:', err);
        return;
    }

    const finalData = JSON.parse(data);

    const sortedData = finalData.sort((a, b) => a.index - b.index);

    const downloadLinks = sortedData.map(item => {
        let link = item.downloadLink;
        link = decodeURIComponent(link);
        return link;
    });

    fs.writeFile('links.json', JSON.stringify(downloadLinks, null, 2), 'utf8', (err) => {
        if (err) {
            console.error('Error saving sorted links:', err);
            return;
        }
    });

    downloadLinks.forEach((link, index) => {
        console.log(`Enlace ${index + 1}: ${link}`);
    });
});
