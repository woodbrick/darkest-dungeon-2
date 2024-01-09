/**
 * @project: 遍历文件目录
 */
const fs = require('fs');

const ScriptSuffixRegex = /^hero\_.+csv$/;
/**
 * [遍历某个文件下的ts]
 *
 * @param {String} pathStr 路径
 * @returns {Array} ["login", "register"]
 */
function getPath(pathStr) {
  const arr = [];
  if (fs.existsSync(pathStr)) {
    const dirPaths = fs.readdirSync(pathStr);
    dirPaths.map((item) => {
      if (ScriptSuffixRegex.test(item)) {
        arr.push(item);
      }
    });
    return arr;
  }
}

/**
 * [获取 entry 文件入口]，将目录下 index.jsx 文件作为入口
 * @param {String} dirPath 路径
 * @returns {Array} ["index.ts"]
 */
module.exports = getPath;
