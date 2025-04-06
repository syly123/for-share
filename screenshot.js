const { app, BrowserWindow, globalShortcut, ipcMain } = require("electron");
const path = require("path");

// モジュール全体を1回だけ require して同じインスタンスを利用する
const nut = require("@nut-tree-fork/nut-js");

function createOverlayWindow() {
  const { width, height } =
    require("electron").screen.getPrimaryDisplay().workAreaSize;
  let overlayWindow = new BrowserWindow({
    x: 0,
    y: 0,
    width,
    height,
    frame: false,
    transparent: true,
    fullscreen: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  overlayWindow.loadFile(path.join(__dirname, "overlay.html"));
  overlayWindow.on("closed", () => {
    overlayWindow = null;
  });
}

ipcMain.on("selection-made", async (event, selection) => {
  console.log("受信した選択範囲:", selection);

  let { x, y, width, height } = selection;
  // 数値に変換（整数に丸める）
  x = Math.floor(Number(x));
  y = Math.floor(Number(y));
  width = Math.floor(Number(width));
  height = Math.floor(Number(height));

  if (isNaN(x) || isNaN(y) || isNaN(width) || isNaN(height)) {
    console.error("不正な値が含まれています:", selection);
    return;
  }
  if (width <= 0 || height <= 0) {
    console.error("幅または高さがゼロ以下です。キャプチャをキャンセルします。");
    return;
  }

  try {
    // 同じ nut モジュールから Region を生成する
    const region = new nut.Region(x, y, width, height);
    console.log(`キャプチャ対象 Region: (${x}, ${y}) ${width}x${height}`);
    console.log("region instanceof nut.Region:", region instanceof nut.Region);
    // ※　ここで region instanceof nut.Region が false なら、同じインスタンスで作れていない可能性があります

    // captureRegion に region を渡す
    const imgBuffer = await nut.screen.captureRegion(region);
    const base64 = imgBuffer.toString("base64");

    // キャプチャ結果表示用ウィンドウを生成
    let ssWindow = new BrowserWindow({
      width: width,
      height: height,
      show: false,
      frame: false,
      transparent: true,
      alwaysOnTop: true,
      resizable: true,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
      },
    });
    ssWindow.loadURL(
      `file://${__dirname}/screenshot.html?img=${encodeURIComponent(base64)}`
    );
    ssWindow.once("ready-to-show", () => {
      ssWindow.show();
    });
  } catch (error) {
    console.error("キャプチャ中のエラー:", error);
  }
});

app.whenReady().then(() => {
  globalShortcut.register("F1", () => {
    createOverlayWindow();
  });
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createOverlayWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
