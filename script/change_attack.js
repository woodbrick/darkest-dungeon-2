// import path from 'path';

const fs = require('fs');

const filePath = './dlc_dul_cru/hero_cru_data_export.Group.csv';
fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    const newStr = data.replace(/key_map\,health_damage\,health_damage_range\,crit_chance\,\r?\nadd_stats\,([\.|\d]+)\,([\.|\d]+)\,([\.|\d]+)\,/g,
        (value,damage,range,crit_chance) => {
            return `key_map,health_damage,health_damage_range,crit_chance,\nadd_stats,${parseInt(damage)-2},${range},${crit_chance/2},`
        }
    )
    fs.writeFileSync(filePath, newStr);

  });
