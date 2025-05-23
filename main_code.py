import tkinter as tk
from PIL import ImageGrab, Image, ImageTk


class ScreenshotOverlay:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.screenshot = None
        self.is_dragging = False

        self.selection_window = tk.Tk()
        self.selection_window.attributes("-fullscreen", True)
        self.selection_window.attributes("-topmost", True)
        self.selection_window.configure(cursor="cross", bg="gray")
        self.selection_window.attributes("-alpha", 0.3)

        self.selection_window.bind("<ButtonPress-1>", self.on_press)
        self.selection_window.bind("<B1-Motion>", self.on_drag)
        self.selection_window.bind("<ButtonRelease-1>", self.on_release)

        self.selection_canvas = tk.Canvas(
            self.selection_window, bg="gray", highlightthickness=0
        )
        self.selection_canvas.pack(fill=tk.BOTH, expand=True)

        self.selection_window.mainloop()

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

        self.screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.selection_window.destroy()
        self.display_screenshot(x1, y1, x2, y2)

    def display_screenshot(self, x1, y1, x2, y2):
        self.root = tk.Tk()
        self.root.geometry(f"{x2-x1}x{y2-y1}+{x1}+{y1}")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.tk_image = ImageTk.PhotoImage(self.screenshot)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)
        self.root.bind("<Escape>", self.close)
        self.root.mainloop()

    def start_move(self, event):
        self.is_dragging = True
        self.root.startX = event.x
        self.root.startY = event.y

    def on_move(self, event):
        if self.is_dragging:
            x = self.root.winfo_x() + (event.x - self.root.startX)
            y = self.root.winfo_y() + (event.y - self.root.startY)
            self.root.geometry(f"+{x}+{y}")

    def close(self, event):
        self.root.destroy()


if __name__ == "__main__":
    ScreenshotOverlay()
