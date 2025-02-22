import tkinter as tk
from tkinter import Event, scrolledtext

import cv2
from PIL import Image, ImageTk

from scene.scene import SceneManager


class OpenCVApp:
    CAM_INDEX = 1

    def __init__(self, root):
        self.root = root
        self.root.title("Rubiks Cube Solver")
        self.root.geometry("1600x800")

        # Sidebar
        self.sidebar = tk.Frame(
            self.root,
            width=200,
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.info_box = scrolledtext.ScrolledText(self.sidebar, height=10, width=30)
        self.info_box.pack(pady=10)

        # Video Frame
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        # OpenCV
        self.cap = None
        self.scene_manager = SceneManager()

        # Keyboard Bindings
        self.root.bind("<Key>", self.handle_keypress)

        # Start
        self.cap = cv2.VideoCapture(self.CAM_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.update_frame()

    def update_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.scene_manager.update(frame)
                self.scene_manager.render_ui(frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk  # type: ignore
                self.video_label.config(image=imgtk)

            self.root.after(10, self.update_frame)

    def handle_keypress(self, event: Event):
        key = event.keysym
        self.scene_manager.handle_input(key)
        self.log_message(f"Key Pressed: {key}")

    def log_message(self, message):
        self.info_box.insert(tk.END, message + "\n")
        self.info_box.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = OpenCVApp(root)
    root.mainloop()
