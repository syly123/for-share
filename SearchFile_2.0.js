const fs = require("fs");
const path = require("path");

// UTF-8 BOM を追加してファイルを作成
const outputFilePath = "C:/Users/tatsu/file_info_node_0515.tsv";
const BOM = "\uFEFF"; // **UTF-8 BOM**
fs.writeFileSync(
  outputFilePath,
  BOM + "Type\tPath\tName\tLast Modified\tCreated\tSize (bytes)\n",
  { encoding: "utf8" }
);

let startDir = String.raw`C:\Users\tatsu\Documents`; // 対象ディレクトリ
startDir = startDir.replace(/\\/g, "/");

// 日付をフォーマットする関数
function formatDate(date) {
  const pad = (num) => String(num).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(
    date.getDate()
  )} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(
    date.getSeconds()
  )}`;
}

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

        fs.appendFileSync(
          outputFilePath,
          `${type}\t${entry.name}\t${fullPath}\t${lastModified}\t${created}\t${size}\n`,
          { encoding: "utf8" }
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
    console.log("Completed"); // **完了時に "Completed" を表示**
  })
  .catch(() => {});
