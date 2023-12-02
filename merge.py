import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageFile
import datetime
import os
import numpy as np
import cv2

ImageFile.LOAD_TRUNCATED_IMAGES = True


class PhotoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.photos = []
        self.points = []
        self.current_photo_index = 0
        self.upload_photo_button = tk.Button(
            self.root, text="Upload Photo", command=self.upload_photo
        )
        self.upload_photo_button.pack()
        self.upload_folder_button = tk.Button(
            self.root, text="Upload Folder", command=self.upload_folder
        )
        self.upload_folder_button.pack()
        # self.select_button = tk.Button(
        #     self.root,
        #     text="Select Point",
        #     state=tk.DISABLED,
        #     command=self.confirm_point,
        # )
        # self.select_button.pack()
        self.next_button = tk.Button(
            self.root, text="Next", state=tk.DISABLED, command=self.next_photo
        )
        self.next_button.pack()
        self.prev_button = tk.Button(
            self.root, text="Previous", state=tk.DISABLED, command=self.prev_photo
        )
        self.prev_button.pack()
        self.generate_button = tk.Button(
            self.root,
            text="Generate",
            state=tk.DISABLED,
            command=self.ask_frame_duration,
        )
        self.generate_button.pack()
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.pack()
        self.root.bind(
            "<Left>", self.prev_photo
        )  # Bind left arrow key to prev_photo function
        self.root.bind(
            "<Right>", self.next_photo
        )  # Bind right arrow key to next_photo function

    def upload_photo(self):
        filepaths = filedialog.askopenfilenames()
        if len(filepaths) + len(self.photos) > 4:
            print("Maximum 4 photos can be uploaded.")
            return
        for filepath in filepaths:
            date = datetime.datetime.now()
            self.photos.append((filepath, date))
        self.photos.sort(key=lambda x: os.path.getmtime(x[0]), reverse=True)
        self.open_photo(self.photos[self.current_photo_index][0])

    def upload_folder(self):
        folderpath = filedialog.askdirectory()
        filepaths = [
            os.path.join(folderpath, f)
            for f in os.listdir(folderpath)
            if f.endswith(".jpg") or f.endswith(".png")
        ]
        if len(filepaths) + len(self.photos) > 4:
            print("Maximum 4 photos can be uploaded.")
            return
        for filepath in filepaths:
            date = datetime.datetime.now()
            self.photos.append((filepath, date))
        self.photos.sort(key=lambda x: os.path.getmtime(x[0]), reverse=True)
        self.open_photo(self.photos[self.current_photo_index][0])

    def open_photo(self, filepath):
        # Destroy the current image if it exists
        if hasattr(self, "canvas"):
            self.canvas.destroy()

        self.img = Image.open(filepath)
        self.original_img_size = self.img.size  # Save the original image size

        # Half the screen width and height
        screen_width, screen_height = (
            self.root.winfo_screenwidth() / 1.3,
            self.root.winfo_screenheight() / 1.3,
        )
        # Calculate the ratio to resize the image to fit within the half screen size
        ratio = min(screen_width / self.img.width, screen_height / self.img.height)
        # Resize the image using the calculated ratio
        self.img = self.img.resize(
            (int(self.img.width * ratio), int(self.img.height * ratio))
        )
        photo = ImageTk.PhotoImage(self.img)
        # Create a canvas with the resized image dimensions
        self.canvas = tk.Canvas(
            self.root, width=self.img.size[0], height=self.img.size[1]
        )
        self.canvas.create_image(0, 0, image=photo, anchor="nw")
        self.canvas.image = photo
        self.canvas.bind("<Button-1>", self.select_point)
        self.canvas.bind(
            "<Motion>", self.show_magnifier
        )  # Bind mouse motion event to show_magnifier function
        self.canvas.bind(
            "<MouseWheel>", self.zoom_image
        )  # Bind mouse wheel event to zoom_image function
        self.canvas.pack()
        # self.select_button.config(state=tk.NORMAL)
        if len(self.photos) > 1:
            self.next_button.config(state=tk.NORMAL)
        # If there exists a point for the photo to be opened, draw the point with select_point
        if len(self.points) > self.current_photo_index:
            point = self.points[self.current_photo_index]
            event = tk.Event()
            event.x = point[0] * (self.canvas.winfo_width() / self.original_img_size[0])
            event.y = point[1] * (
                self.canvas.winfo_height() / self.original_img_size[1]
            )
            self.select_point(event)

    def show_magnifier(self, event):
        # Create a magnifier glass on the cursor when hovering over the image
        if hasattr(self, "magnifier"):
            self.canvas.delete(self.magnifier)
        magnifier_size = 200  # Size of the magnifier glass
        magnified_img = self.img.crop(
            (
                event.x - magnifier_size // 2,
                event.y - magnifier_size // 2,
                event.x + magnifier_size // 2,
                event.y + magnifier_size // 2,
            )
        ).resize((magnifier_size * 2, magnifier_size * 2))
        self.magnifier = ImageTk.PhotoImage(magnified_img)
        self.canvas.create_image(event.x, event.y, image=self.magnifier)
        # If a point has been selected, show it on the magnifier
        if hasattr(self, "point"):
            point_x = self.point[0] * (
                self.canvas.winfo_width() / self.original_img_size[0]
            )
            point_y = self.point[1] * (
                self.canvas.winfo_height() / self.original_img_size[1]
            )
            if (
                abs(event.x - point_x) <= magnifier_size // 2
                and abs(event.y - point_y) <= magnifier_size // 2
            ):
                # Delete the previous point if it exists
                if hasattr(self, "point_text"):
                    self.canvas.delete(self.point_text)
                self.point_text = self.canvas.create_text(
                    event.x + (point_x - event.x) * 2,
                    event.y + (point_y - event.y) * 2,
                    text="x",
                    fill="red",
                )

    def zoom_image(self, event):
        # Zoom in when the mouse wheel is scrolled up, and zoom out when it is scrolled down
        if event.delta > 0:
            self.canvas.scale("all", 0, 0, 1.1, 1.1)
        else:
            self.canvas.scale("all", 0, 0, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def select_point(self, event):
        if hasattr(self, "point"):
            self.canvas.delete(self.point_text)
        # Rescale the points to match the original image dimensions
        self.point = (
            event.x * (self.original_img_size[0] / self.canvas.winfo_width()),
            event.y * (self.original_img_size[1] / self.canvas.winfo_height()),
        )
        print("Selected point:", self.point)
        self.point_text = self.canvas.create_text(
            event.x, event.y, text="x", fill="red"
        )

    def confirm_point(self):
        if hasattr(self, "point"):
            self.points.append(self.point)
            if len(self.photos) == len(self.points):
                self.generate_button.config(state=tk.NORMAL)

    def next_photo(self, event=None):
        self.confirm_point()
        if self.current_photo_index < len(self.photos) - 1:
            self.current_photo_index += 1
            self.open_photo(self.photos[self.current_photo_index][0])
            self.prev_button.config(state=tk.NORMAL)
        if self.current_photo_index == len(self.photos) - 1:
            self.next_button.config(state=tk.DISABLED)

    def prev_photo(self, event=None):
        if self.current_photo_index > 0:
            self.current_photo_index -= 1
            self.open_photo(self.photos[self.current_photo_index][0])
            self.next_button.config(state=tk.NORMAL)
        if self.current_photo_index == 0:
            self.prev_button.config(state=tk.DISABLED)

    def ask_frame_duration(self):
        self.frame_duration = simpledialog.askinteger(
            "Input", "Enter frame duration (in ms):", parent=self.root
        )
        self.align_and_generate()

    def align_and_generate(self):
        # Ensure there is a reference point and at least one other point to align
        if len(self.points) < 2:
            print("Not enough points to align.")
            return

        # The reference point will be the first one selected
        ref_point = np.array(self.points[0], dtype="float32")

        # Initialize an array to hold the transformed images
        transformed_images = []

        for i, (path, date) in enumerate(self.photos):
            # Open the image
            img = cv2.imread(path)
            selected_point = np.array(self.points[i], dtype="float32")

            # Calculate the translation matrix
            dx, dy = ref_point - selected_point
            M = np.float32([[1, 0, dx], [0, 1, dy]])

            # Apply the translation
            transformed_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

            # Save the transformed image for GIF creation
            transformed_images.append(transformed_img)

        # Now create the GIF with the transformed images
        self.create_gif(transformed_images)

    def create_gif(self, images):
        gif_images = [
            Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) for img in images
        ]
        gif_images += gif_images[-2:0:-1]
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        gif_path = f"/Users/hudzah/Documents/Generated/generated_{timestamp}.gif"
        gif_images[0].save(
            gif_path,
            save_all=True,
            append_images=gif_images[1:],
            duration=self.frame_duration,
            loop=0,
        )
        print("GIF saved at:", gif_path)

    def reset(self):
        self.photos = []
        self.points = []
        self.current_photo_index = 0
        if hasattr(self, "canvas"):
            self.canvas.delete("all")
        print("All photos, points, and canvas have been cleared.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PhotoApp()
    app.run()
