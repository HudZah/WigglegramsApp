# 3DSync

3DSync is a Python application that allows you to upload, view, and align multiple images. This is ideal for creating 3D gif effects from Cameras like Nishika N8000 and Reto 3D. It provides a user-friendly interface to select specific points in each image, aligns the images based on these points, and generates a GIF from the aligned images. 


Create gifs like these!

https://github.com/HudZah/3DSync/assets/56107325/75e9a4b1-d8c6-4de2-b440-a1d8b89e7b42

## Features

- Upload individual photos or an entire folder of photos.
- Navigate through uploaded photos.
- Select a specific point in each photo.
- Automatically aligns photos based on selected points.
- Generate a GIF from the aligned photos.

## Installation

Ensure you have Python 3.6 or later installed.

Clone the repository:
```
git clone https://github.com/your-username/3DSync.git
```
Navigate to the cloned project directory:
```
cd 3DSync
```
## Usage

### Step 1: Launch the Application

Run the application by executing the following command in your terminal:
```
python3 merge.py
```
Modify the ```gif_path``` to where you want your generated gif to go to.

### Step 2: Upload Photos

Click on the "Upload Photo" button to upload individual photos or "Upload Folder" to upload an entire folder of photos. Note that a maximum of 4 photos can be uploaded.

### Step 3: Navigate Through Photos

Use the "Next" and "Previous" buttons to navigate through the uploaded photos.

### Step 4: Select Points

Click on a specific point in each photo. This point will be used to align the photos. The selected point will be marked with a red 'x'.

### Step 5: Generate GIF

Once you have selected a point in each photo, click on the "Generate" button. You will be prompted to enter a frame duration (in milliseconds) for the GIF. After entering the frame duration, the application will align the photos and generate a GIF.

### Step 6: Reset

If you want to start over, click on the "Reset" button. This will clear all uploaded photos and selected points.

Remember, the application aligns the photos based on the selected points and generates a GIF from the aligned photos. The GIF will be saved in the specified directory and the path will be printed in the console.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
