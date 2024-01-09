const path = require("path");
const fs = require("fs");

const getPath = require("./entry-path");
const dirPath = path.resolve("./");
const dirPathDlc = path.resolve("./dlc_dul_cru/");
const paths = getPath(dirPath).map(pathStr => path.resolve("./", pathStr));;
const dlcPaths = getPath(dirPathDlc).map(pathStr => path.resolve("./dlc_dul_cru/", pathStr));
const allHeroPaths = paths.concat(dlcPaths).filter(path => path !== 'hero_rules_data_export');
console.log(allHeroPaths);

allHeroPaths.forEach((path) => {
  // updateFileAttributes(path)
})

const DefaultHealthHeader = 'key_map,health_max,speed,stress_max,deaths_door_chance,speed_number_of_turns,health_heal_percent_between_nodes,route_choice_chance,';

const updateFileAttributes = (filePath) => {
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    const newStr = data.replace(
      /DefaultHealthHeader\r?\nadd_stats\,([\.|\d]+)\,([\.|\d]+)\,([\.|\d]+)\,/g,
      (value, health_max, speed, stress_max, deaths_door_chance, speed_number_of_turns, health_heal_percent_between_nodes, route_choice_chance) => {
        // add_stats,40,5,10,1,1,0.1,0.67,
        return `${DefaultHealthHeader}\nadd_stats,${health_max + 4},${speed},${stress_max},${deaths_door_chance},${speed_number_of_turns},${health_heal_percent_between_nodes},${route_choice_chance},`;
      }
    );
    // const newStr = data.replace(
    //   /key_map\,health_damage\,health_damage_range\,crit_chance\,\r?\nadd_stats\,([\.|\d]+)\,([\.|\d]+)\,([\.|\d]+)\,/g,
    //   (value, damage, range, crit_chance) => {
    //     return `key_map,health_damage,health_damage_range,crit_chance,\nadd_stats,${
    //       parseInt(damage) - 2
    //     },${range},${crit_chance / 2},`;
    //   }
    // );

    fs.writeFileSync(filePath, newStr);
  });
}

