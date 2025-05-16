const fs = require("fs");
const path = require("path");

// 日付をフォーマットする関数
function formatDate(date) {
  const pad = (num) => String(num).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(
    date.getDate()
  )} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(
    date.getSeconds()
  )}`;
}

const outputFilePath = "C:/Users/tatsu/file_info_node_0515.tsv";
let startDir = String.raw`C:\Users\tatsu\Documents`; // 対象ディレクトリを指定
startDir = startDir.replace(/\\/g, "/");

const writeStream = fs.createWriteStream(outputFilePath);
writeStream.write("Type\tPath\tName\tLast Modified\tCreated\tSize (bytes)\n");

// 非同期で並列処理を最適化
async function getFileInfo(dir) {
  try {
    const entries = await fs.promises.readdir(dir, { withFileTypes: true });

    const tasks = entries.map(async (entry) => {
      const fullPath = path.join(dir, entry.name);

      try {
        const stats = await fs.promises.stat(fullPath);
        const type = entry.isDirectory() ? "Folder" : "File";
        const lastModified = formatDate(stats.mtime);
        const created = formatDate(stats.birthtime);
        const size = entry.isDirectory() ? "-" : stats.size;

        writeStream.write(
          `${type}\t${fullPath}\t${entry.name}\t${lastModified}\t${created}\t${size}\n`
        );

        if (entry.isDirectory()) {
          await getFileInfo(fullPath);
        }
      } catch (err) {
        // スキップしてエラーハンドリングを最適化
      }
    });

    await Promise.all(tasks); // **並列処理で速度向上**
  } catch (err) {
    // ルートディレクトリの読み込み失敗を最適化
  }
}

// 実行
getFileInfo(startDir)
  .then(() => {
    writeStream.end();
    console.log("Completed"); // **完了時に "Completed" を表示**
  })
  .catch(() => {});
