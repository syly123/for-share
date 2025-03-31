const fs = require("fs");
const path = require("path");
const { promisify } = require("util");

const outputFilePath = "file_info_node.csv";
const startDir = "C:/your/target/directory"; // ここに対象ディレクトリを指定

const writeStream = fs.createWriteStream(outputFilePath);
writeStream.write("Type,Path,Name,Last Modified,Created,Size (bytes)\n");

async function getFileInfo(dir) {
  const entries = await fs.promises.readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const stats = await fs.promises.stat(fullPath);

    const type = entry.isDirectory() ? "Folder" : "File";
    const lastModified = stats.mtime.toISOString();
    const created = stats.birthtime.toISOString();
    const size = entry.isDirectory() ? "-" : stats.size;

    writeStream.write(
      `${type},${fullPath},${entry.name},${lastModified},${created},${size}\n`
    );

    if (entry.isDirectory()) {
      await getFileInfo(fullPath);
    }
  }
}

// 実行
getFileInfo(startDir)
  .then(() => {
    console.log("File information saved to", outputFilePath);
    writeStream.end();
  })
  .catch((err) => console.error("Error:", err));
