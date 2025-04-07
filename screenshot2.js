const {
  app,
  BrowserWindow,
  globalShortcut,
  desktopCapturer,
  screen: electronScreen,
} = require("electron");
const { screen: nutScreen, mouse } = require("@nut-tree-fork/nut-js");
const path = require("path");

console.log("Starting Electron app...");

app.on("ready", async () => {
  console.log("App is ready!");
  const screenshotWindows = new Map();
  let isSelecting = false;
  let startPoint = null;
  let selectionWindow = null;
  let currentWindowId = 0;

  // nut.jsの設定（マウス位置取得用）
  try {
    nutScreen.config.autoHighlight = false;
    console.log("nut.js configured successfully");
  } catch (err) {
    console.error("nut.js config error:", err);
  }

  // F1で選択開始
  const f1Registered = globalShortcut.register("F1", async () => {
    if (!isSelecting) {
      console.log("F1 pressed, starting screenshot selection...");
      try {
        isSelecting = true;
        startPoint = await mouse.getPosition();
        console.log("Selection started at:", startPoint);

        selectionWindow = new BrowserWindow({
          frame: false,
          transparent: true,
          alwaysOnTop: true,
          webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, "preload.js"),
          },
        });
        selectionWindow.loadURL(
          'data:text/html,<body style="margin:0;background:rgba(0,0,255,0.2);"></body>'
        );
        selectionWindow.setMenu(null);
        console.log("Selection window created");

        const updateSelection = setInterval(async () => {
          if (!isSelecting || !selectionWindow) {
            clearInterval(updateSelection);
            return;
          }
          const currentPoint = await mouse.getPosition();
          const x = Math.min(startPoint.x, currentPoint.x);
          const y = Math.min(startPoint.y, currentPoint.y);
          const width = Math.abs(currentPoint.x - startPoint.x);
          const height = Math.abs(currentPoint.y - startPoint.y);
          selectionWindow.setBounds({ x, y, width, height });
        }, 50);

        console.log("Press Enter to complete selection...");
      } catch (err) {
        console.error("Error starting selection:", err);
        isSelecting = false;
        if (selectionWindow) selectionWindow.close();
      }
    } else {
      console.log("F1 pressed, but already selecting");
    }
  });
  if (!f1Registered) console.error("Failed to register F1 shortcut");
  else console.log("F1 shortcut registered successfully");

  // Enterで範囲確定
  const enterRegistered = globalShortcut.register("Enter", async () => {
    if (isSelecting) {
      console.log("Enter pressed, completing screenshot...");
      try {
        const endPoint = await mouse.getPosition();
        console.log("Selection ended at:", endPoint);

        const x = Math.min(startPoint.x, endPoint.x);
        const y = Math.min(startPoint.y, endPoint.y);
        const width = Math.abs(endPoint.x - startPoint.x);
        const height = Math.abs(endPoint.y - startPoint.y);

        if (width < 5 || height < 5) {
          console.log("Selection too small, aborting");
          isSelecting = false;
          if (selectionWindow) selectionWindow.close();
          selectionWindow = null;
          return;
        }

        if (selectionWindow) {
          selectionWindow.close();
          selectionWindow = null;
        }

        console.log("Capturing screen with desktopCapturer...");
        const sources = await desktopCapturer.getSources({
          types: ["screen"],
          thumbnailSize: {
            width: electronScreen.getPrimaryDisplay().workAreaSize.width,
            height: electronScreen.getPrimaryDisplay().workAreaSize.height,
          },
        });
        const source = sources[0];
        const screenshot = source.thumbnail;

        console.log("Cropping region:", { x, y, width, height });
        const croppedImage = screenshot.crop({ x, y, width, height });
        const buffer = croppedImage.toPNG();
        console.log("Screenshot captured, size:", buffer.length);

        const win = new BrowserWindow({
          width: width,
          height: height,
          x: x,
          y: y,
          frame: false,
          alwaysOnTop: true,
          transparent: true,
          webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, "preload.js"),
          },
        });

        win.loadURL(
          `data:text/html,<body style="margin:0"><img src="data:image/png;base64,${buffer.toString(
            "base64"
          )}" style="width:100%;height:100%;-webkit-user-drag:none;"></body>`
        );
        win.setMenu(null);
        console.log("Screenshot window created at:", x, y);

        const windowId = `screenshot_${currentWindowId++}`;
        screenshotWindows.set(windowId, win);

        const { ipcMain } = require("electron");
        ipcMain.on("drag-start", () => {
          console.log("Drag started");
        });
        ipcMain.on("drag-move", (event, { dx, dy }) => {
          const currentPos = win.getPosition();
          win.setPosition(currentPos[0] + dx, currentPos[1] + dy);
          console.log("Dragging to:", currentPos[0] + dx, currentPos[1] + dy);
        });
        ipcMain.on("drag-end", () => {
          console.log("Drag ended");
        });
        ipcMain.on("close-window", () => {
          win.close();
          screenshotWindows.delete(windowId);
          console.log("Window closed:", windowId);
        });

        win.on("closed", () => {
          screenshotWindows.delete(windowId);
        });

        isSelecting = false;
      } catch (err) {
        console.error("Error completing screenshot:", err);
        isSelecting = false;
        if (selectionWindow) selectionWindow.close();
        selectionWindow = null;
      }
    }
  });
  if (!enterRegistered) console.error("Failed to register Enter shortcut");
  else console.log("Enter shortcut registered successfully");

  // テストウィンドウ
  try {
    const testWin = new BrowserWindow({
      width: 400,
      height: 300,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, "preload.js"),
      },
    });
    testWin.loadURL("data:text/html,<h1>Test Window - Press F1 to Start</h1>");
    console.log("Test window created");
  } catch (err) {
    console.error("Error creating test window:", err);
  }

  console.log("App initialized, press F1 to start screenshot selection...");
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("will-quit", () => {
  globalShortcut.unregisterAll();
  console.log("App quitting, shortcuts unregistered");
});
