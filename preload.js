const { ipcRenderer } = require("electron");

document.addEventListener("mousedown", (event) => {
  let startX = event.clientX;
  let startY = event.clientY;

  const onMouseMove = (moveEvent) => {
    let dx = moveEvent.clientX - startX;
    let dy = moveEvent.clientY - startY;
    ipcRenderer.send("drag-move", { dx, dy });
    startX = moveEvent.clientX;
    startY = moveEvent.clientY;
  };

  const onMouseUp = () => {
    document.removeEventListener("mousemove", onMouseMove);
    document.removeEventListener("mouseup", onMouseUp);
    ipcRenderer.send("drag-end");
  };

  document.addEventListener("mousemove", onMouseMove);
  document.addEventListener("mouseup", onMouseUp);
});
