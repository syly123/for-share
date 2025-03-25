import tkinter as tk
from PIL import ImageGrab, Image, ImageTk


class ScreenshotOverlay:
    instances = []  # スクリーンショットのインスタンスを管理

    def __init__(self, screenshot=None, x1=0, y1=0, x2=0, y2=0):
        if screenshot is None:
            self.start_selection()
        else:
            self.screenshot = screenshot
            self.display_screenshot(x1, y1, x2, y2)

    def start_selection(self):
        self.start_x = None
        self.start_y = None
        self.rect = None

        self.selection_window = tk.Toplevel()
        self.selection_window.attributes("-fullscreen", True)
        self.selection_window.attributes("-topmost", True)
        self.selection_window.configure(cursor="cross", bg="gray")
        self.selection_window.attributes("-alpha", 0.3)

        self.selection_canvas = tk.Canvas(
            self.selection_window, bg="gray", highlightthickness=0
        )
        self.selection_canvas.pack(fill=tk.BOTH, expand=True)

        self.selection_window.bind("<ButtonPress-1>", self.on_press)
        self.selection_window.bind("<B1-Motion>", self.on_drag)
        self.selection_window.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.selection_canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2,
        )

    def on_drag(self, event):
        self.selection_canvas.coords(
            self.rect, self.start_x, self.start_y, event.x, event.y
        )

    def on_release(self, event):
        self.selection_window.withdraw()
        x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.selection_window.destroy()
        ScreenshotOverlay(screenshot, x1, y1, x2, y2)

    def display_screenshot(self, x1, y1, x2, y2):
        self.root = tk.Toplevel()
        self.root.geometry(f"{x2-x1}x{y2-y1}+{x1}+{y1}")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.tk_image = ImageTk.PhotoImage(self.screenshot)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)
        self.root.bind("<ButtonRelease-1>", self.focus_window)
        self.root.bind("<Escape>", self.close)

        ScreenshotOverlay.instances.append(self.root)

    def start_move(self, event):
        self.is_dragging = True
        self.root.startX = event.x
        self.root.startY = event.y

    def on_move(self, event):
        if self.is_dragging:
            x = self.root.winfo_x() + (event.x - self.root.startX)
            y = self.root.winfo_y() + (event.y - self.root.startY)
            self.root.geometry(f"+{x}+{y}")

    def focus_window(self, event):
        self.root.attributes("-topmost", True)
        self.root.focus_force()

    def close(self, event):
        self.root.destroy()
        ScreenshotOverlay.instances.remove(self.root)


def start_screenshot(event):
    ScreenshotOverlay()


def run_gui():
    root = tk.Tk()
    root.geometry(
        "1x1+0+0"
    )  # ウィンドウは1x1ピクセルのサイズで表示し、目立たないようにする

    def handle_f3(event):
        start_screenshot(event)  # F3が押されるたびにスクリーンショットを取る

    root.bind("<F3>", handle_f3)  # F3で新しいスクリーンショットを作成
    root.mainloop()


if __name__ == "__main__":
    run_gui()
