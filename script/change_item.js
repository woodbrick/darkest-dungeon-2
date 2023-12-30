


const fs = require('fs');

const filePath = './item_data_export.Group.csv';
fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    const newStr = data.replace(/m_maxQty,(\d+),/g,
        (value,qty) => {
            return `m_maxQty,${parseInt(qty)*2},`
        }
    )
    fs.writeFileSync(filePath, newStr);

  });
