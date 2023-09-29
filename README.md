# Digital Image Processing Web App

This is a web application for performing digital image processing tasks using OpenCV and Flask. With this app, you can apply various image filters, transformations, and enhancements to your images through a user-friendly web interface.

## Features

### Umum (General)
- **Normal**: Apply no processing, display the original image.
- **Grayscale**: Convert the image to grayscale.
- **Zoom In**: Zoom in on the image.
- **Zoom Out**: Zoom out from the image.

### Pergeseran (Translation)
- **Kiri (Left)**: Shift the image to the left.
- **Kanan (Right)**: Shift the image to the right.
- **Atas (Up)**: Shift the image upwards.
- **Bawah (Down)**: Shift the image downwards.

### Penerangan (Brightness)
- **Terang (*)**: Multiply the brightness of the image.
- **Gelap (/)**: Divide the brightness of the image.
- **Terang (+)**: Add to the brightness of the image.
- **Gelap (-)**: Subtract from the brightness of the image.

### Analisis Gambar (Image Analysis)
- **Histogram**: Display the histogram of the image (RGB).

### Pemrosesan Gambar (Image Processing)
- **Histogram Equalizer**: Apply histogram equalization to enhance image contrast.

### Filter Gambar (Image Filters)
- **Edge Detection**: Detect edges in the image.
- **Blur**: Apply blurring to the image.
- **Sharpening**: Enhance image sharpness.

### Thresholding
- **Thresholding**: Apply binary thresholding to the image based on provided thresholds.

### Blur (Week 6)
- **Average Blur**: Apply average blurring.
- **Median Blur**: Apply median blurring with a custom kernel size.
- **Gaussian Blur**: Apply Gaussian blurring with a custom kernel size.

### Filter (Week 6)
- **Bilateral Filter**: Apply bilateral filtering.
- **Zero Padding**: Apply zero padding.

### Convolution Filter (Week 6)
- **Lowpass Filter**: Apply a lowpass filter with a custom kernel size.
- **Highpass Filter**: Apply a highpass filter with a custom kernel size.
- **Bandpass Filter**: Apply a bandpass filter with a custom kernel size.

## Prerequisites

Before running this application, ensure you have the following dependencies installed:

- Python 3.x
- Flask
- OpenCV

You can install these dependencies using `pip`. For example:

```shell
pip install Flask opencv-python
```
# Getting Started
## 1. Clone this repository to your local machine:
```shell
git clone https://github.com/deo23/digital-image-processing-python-webapp.git
cd digital-image-processing-python-webapp
```

## 2. Run the Flask application:
```shell
python app.py
```

## 3. Open a web browser and navigate to http://localhost:5000 to access the web app.
