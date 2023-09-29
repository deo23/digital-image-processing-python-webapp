import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math
from collections import Counter
from pylab import savefig
import cv2
import matplotlib

matplotlib.use("Agg")


def grayscale():
    if not is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)
        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]
        new_arr = r.astype(int) + g.astype(int) + b.astype(int)
        new_arr = (new_arr / 3).astype("uint8")
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")


def is_grey_scale(img_path):
    im = Image.open(img_path).convert("RGB")
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True


def zoomin():
    if is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)

        if len(img_arr.shape) == 3:
            # Convert grayscale to 2D array
            img_arr = img_arr[:, :, 0]

        new_size = (img_arr.shape[0] * 2, img_arr.shape[1] * 2)
        new_arr = np.full(new_size, 255, dtype=np.uint8)

        for i in range(len(img_arr)):
            for j in range(len(img_arr[i])):
                new_arr[2 * i, 2 * j] = img_arr[i, j]
                new_arr[2 * i, 2 * j + 1] = img_arr[i, j]
                new_arr[2 * i + 1, 2 * j] = img_arr[i, j]
                new_arr[2 * i + 1, 2 * j + 1] = img_arr[i, j]

        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")
    else:
        img = Image.open("static/img/img_now.jpg")
        img = img.convert("RGB")
        img_arr = np.asarray(img)
        new_size = ((img_arr.shape[0] * 2), (img_arr.shape[1] * 2), img_arr.shape[2])
        new_arr = np.full(new_size, 255)
        new_arr.setflags(write=1)

        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]

        new_r = []
        new_g = []
        new_b = []

        for row in range(len(r)):
            temp_r = []
            temp_g = []
            temp_b = []
            for i in r[row]:
                temp_r.extend([i, i])
            for j in g[row]:
                temp_g.extend([j, j])
            for k in b[row]:
                temp_b.extend([k, k])
            for _ in (0, 1):
                new_r.append(temp_r)
                new_g.append(temp_g)
                new_b.append(temp_b)

        for i in range(len(new_arr)):
            for j in range(len(new_arr[i])):
                new_arr[i, j, 0] = new_r[i][j]
                new_arr[i, j, 1] = new_g[i][j]
                new_arr[i, j, 2] = new_b[i][j]

        new_arr = new_arr.astype("uint8")
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")


def zoomout():
    if is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)

        if len(img_arr.shape) == 3:
            # Convert grayscale to 2D array
            img_arr = img_arr[:, :, 0]

        x, y = img_arr.shape
        new_arr = np.zeros((int(x / 2), int(y / 2)), dtype=np.uint8)

        for i in range(0, int(x / 2)):
            for j in range(0, int(y / 2)):
                new_arr[i, j] = np.mean(img_arr[2 * i : 2 * i + 2, 2 * j : 2 * j + 2])

        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")
    else:
        img = Image.open("static/img/img_now.jpg")
        img = img.convert("RGB")
        x, y = img.size
        new_arr = Image.new("RGB", (int(x / 2), int(y / 2)))
        r = [0, 0, 0, 0]
        g = [0, 0, 0, 0]
        b = [0, 0, 0, 0]

        for i in range(0, int(x / 2)):
            for j in range(0, int(y / 2)):
                r[0], g[0], b[0] = img.getpixel((2 * i, 2 * j))
                r[1], g[1], b[1] = img.getpixel((2 * i + 1, 2 * j))
                r[2], g[2], b[2] = img.getpixel((2 * i, 2 * j + 1))
                r[3], g[3], b[3] = img.getpixel((2 * i + 1, 2 * j + 1))
                new_arr.putpixel(
                    (int(i), int(j)),
                    (
                        int((r[0] + r[1] + r[2] + r[3]) / 4),
                        int((g[0] + g[1] + g[2] + g[3]) / 4),
                        int((b[0] + b[1] + b[2] + b[3]) / 4),
                    ),
                )
        new_arr = np.uint8(new_arr)
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")


def move_left():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale("static/img/img_now.jpg"):
        g = img_arr[:, :]
        g = np.pad(g, ((0, 0), (0, 50)), "constant")[:, 50:]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 0), (0, 50)), "constant")[:, 50:]
        g = np.pad(g, ((0, 0), (0, 50)), "constant")[:, 50:]
        b = np.pad(b, ((0, 0), (0, 50)), "constant")[:, 50:]
        new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_right():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale("static/img/img_now.jpg"):
        g = img_arr[:, :]
        g = np.pad(g, ((0, 0), (50, 0)), "constant")[:, :-50]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 0), (50, 0)), "constant")[:, :-50]
        g = np.pad(g, ((0, 0), (50, 0)), "constant")[:, :-50]
        b = np.pad(b, ((0, 0), (50, 0)), "constant")[:, :-50]
        new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_up():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale("static/img/img_now.jpg"):
        g = img_arr[:, :]
        g = np.pad(g, ((0, 50), (0, 0)), "constant")[50:, :]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 50), (0, 0)), "constant")[50:, :]
        g = np.pad(g, ((0, 50), (0, 0)), "constant")[50:, :]
        b = np.pad(b, ((0, 50), (0, 0)), "constant")[50:, :]
        new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_down():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale("static/img/img_now.jpg"):
        g = img_arr[:, :]
        g = np.pad(g, ((50, 0), (0, 0)), "constant")[0:-50, :]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((50, 0), (0, 0)), "constant")[0:-50, :]
        g = np.pad(g, ((50, 0), (0, 0)), "constant")[0:-50, :]
        b = np.pad(b, ((50, 0), (0, 0)), "constant")[0:-50, :]
        new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_addition():
    img = Image.open("static/img/img_now.jpg")

    # Check if the image has an alpha channel (transparency)
    if img.mode == "RGBA":
        # Convert the RGBA image to RGB
        img = img.convert("RGB")

    img_arr = np.asarray(img).astype("int16")
    img_arr += 100
    img_arr = np.clip(img_arr, 0, 255).astype("uint8")

    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_substraction():
    img = Image.open("static/img/img_now.jpg")

    if img.mode == "RGBA":
        img = img.convert("RGB")

    img_arr = np.asarray(img).astype("int16")
    img_arr -= 100
    img_arr = np.clip(img_arr, 0, 255).astype("uint8")

    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_multiplication():
    img = Image.open("static/img/img_now.jpg")

    if img.mode == "RGBA":
        img = img.convert("RGB")

    img_arr = np.asarray(img).astype("float32")  # Use float32 for multiplication
    img_arr *= 1.25
    img_arr = np.clip(img_arr, 0, 255).astype("uint8")

    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_division():
    img = Image.open("static/img/img_now.jpg")

    if img.mode == "RGBA":
        img = img.convert("RGB")

    img_arr = np.asarray(img).astype("float32")  # Use float32 for division
    img_arr /= 1.25
    img_arr = np.clip(img_arr, 0, 255).astype("uint8")

    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_now.jpg")


# Make similar updates for other image processing functions


def convolution(img, kernel):
    if len(img.shape) == 3 and img.shape[2] == 3:  # Color image
        h_img, w_img, _ = img.shape
        out = np.zeros((h_img - 2, w_img - 2), dtype=np.float64)
        new_img = np.zeros((h_img - 2, w_img - 2, 3))
        if np.array_equal((img[:, :, 1], img[:, :, 0]), img[:, :, 2]) == True:
            array = img[:, :, 0]
            for h in range(h_img - 2):
                for w in range(w_img - 2):
                    S = np.multiply(array[h : h + 3, w : w + 3], kernel)
                    out[h, w] = np.sum(S)
            out_ = np.clip(out, 0, 255)
            for channel in range(3):
                new_img[:, :, channel] = out_
        else:
            for channel in range(3):
                array = img[:, :, channel]
                for h in range(h_img - 2):
                    for w in range(w_img - 2):
                        S = np.multiply(array[h : h + 3, w : w + 3], kernel)
                        out[h, w] = np.sum(S)
                out_ = np.clip(out, 0, 255)
                new_img[:, :, channel] = out_
        new_img = np.uint8(new_img)
        return new_img

    elif len(img.shape) == 2:  # Grayscale image
        h_img, w_img = img.shape
        out = np.zeros((h_img - 2, w_img - 2), dtype=np.float64)

        for h in range(h_img - 2):
            for w in range(w_img - 2):
                S = np.multiply(img[h : h + 3, w : w + 3], kernel)
                out[h, w] = np.sum(S)

        out_ = np.clip(out, 0, 255)
        new_img = np.uint8(out_)
        return new_img

    else:
        raise ValueError("Unsupported image format")


def edge_detection():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int32)  # Use np.int32 for integer data type
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr.astype(np.uint8))  # Convert back to uint8
    new_img.save("static/img/img_now.jpg")


def blur():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int32)  # Use np.int32 for integer data type
    kernel = np.array(
        [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]]
    )
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr.astype(np.uint8))  # Convert back to uint8
    new_img.save("static/img/img_now.jpg")


def sharpening():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int32)  # Use np.int32 for integer data type
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr.astype(np.uint8))  # Convert back to uint8
    new_img.save("static/img/img_now.jpg")


def histogram_rgb():
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :].flatten()
        data_g = Counter(g)
        plt.bar(list(data_g.keys()), data_g.values(), color="black")
        plt.savefig(f"static/img/grey_histogram.jpg", dpi=300)
        plt.clf()
    else:
        r = img_arr[:, :, 0].flatten()
        g = img_arr[:, :, 1].flatten()
        b = img_arr[:, :, 2].flatten()
        data_r = Counter(r)
        data_g = Counter(g)
        data_b = Counter(b)
        data_rgb = [data_r, data_g, data_b]
        warna = ["red", "green", "blue"]
        data_hist = list(zip(warna, data_rgb))
        for data in data_hist:
            plt.bar(list(data[1].keys()), data[1].values(), color=f"{data[0]}")
            plt.savefig(f"static/img/{data[0]}_histogram.jpg", dpi=300)
            plt.clf()


def df(img):  # to make a histogram (count distribution frequency)
    values = [0] * 256
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            values[img[i, j]] += 1
    return values


def cdf(hist):  # cumulative distribution frequency
    cdf = [0] * len(hist)  # len(hist) is 256
    cdf[0] = hist[0]
    for i in range(1, len(hist)):
        cdf[i] = cdf[i - 1] + hist[i]
    # Now we normalize the histogram
    # What your function h was doing before
    cdf = [ele * 255 / cdf[-1] for ele in cdf]
    return cdf


def histogram_equalizer():
    img = cv2.imread("static\img\img_now.jpg", 0)
    my_cdf = cdf(df(img))
    # use linear interpolation of cdf to find new pixel values. Scipy alternative exists
    image_equalized = np.interp(img, range(0, 256), my_cdf)
    cv2.imwrite("static/img/img_now.jpg", image_equalized)


def threshold(lower_thres, upper_thres):
    img = Image.open("static/img/img_now.jpg")

    # Convert RGBA image to RGB
    img = img.convert("RGB")

    img_arr = np.array(img)
    img_arr.setflags(write=1)  # Ensure the array is writable
    condition = np.logical_and(
        np.greater_equal(img_arr, lower_thres), np.less_equal(img_arr, upper_thres)
    )
    print(lower_thres, upper_thres)
    img_arr[condition] = 255
    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_now.jpg")


# Praktikum 6
def average_blur():
    image = cv2.imread("static/img/img_now.jpg")
    kernel = np.ones((3, 3), np.float32) / 9
    cv_average = cv2.filter2D(image, -1, kernel)
    cv2.imwrite("static/img/img_now.jpg", cv_average)


def median_blur(ksize):
    image = cv2.imread("static/img/img_now.jpg")
    cv_median = cv2.medianBlur(image, ksize)
    cv2.imwrite("static/img/img_now.jpg", cv_median)


def gaussian_blur(ksize):
    image = cv2.imread("static/img/img_now.jpg")
    cv_gaussian = cv2.GaussianBlur(image, (ksize, ksize), 0)
    cv2.imwrite("static/img/img_now.jpg", cv_gaussian)


def bilateral_filter():
    image = cv2.imread("static/img/img_now.jpg")
    cv_bilateral = cv2.bilateralFilter(image, 9, 75, 75)
    cv2.imwrite("static/img/img_now.jpg", cv_bilateral)


def zero_padding():
    image = cv2.imread("static/img/img_now.jpg")
    cv_zero = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    cv2.imwrite("static/img/img_now.jpg", cv_zero)


def lowpass_filter(size):
    image = cv2.imread("static/img/img_now.jpg")

    # Define kernel size and generate a random kernel
    kernel_size = size
    random_kernel = np.random.rand(kernel_size, kernel_size)
    random_kernel /= np.sum(random_kernel)  # Normalize the kernel

    cv_lowpass = cv2.filter2D(image, -1, random_kernel)
    cv2.imwrite("static/img/img_now.jpg", cv_lowpass)


def highpass_filter(size):
    image = cv2.imread("static/img/img_now.jpg")

    # Define kernel size and generate a random kernel
    kernel_size = size
    random_kernel = np.random.randint(-1, 2, size=(kernel_size, kernel_size))
    random_kernel[1, 1] = (
        -np.sum(random_kernel) + 1
    )  # Adjust center element to make the sum zero

    cv_highpass = cv2.filter2D(image, -1, random_kernel)
    cv2.imwrite("static/img/img_now.jpg", cv_highpass)


def bandpass_filter(size):
    image = cv2.imread("static/img/img_now.jpg")

    # Define kernel size and generate a random kernel
    kernel_size = size
    random_kernel = np.random.randint(-1, 2, size=(kernel_size, kernel_size))

    while np.sum(random_kernel) == 0:
        random_kernel = np.random.randint(-1, 2, size=(kernel_size, kernel_size))

    cv_bandpass = cv2.filter2D(image, -1, random_kernel)
    cv2.imwrite("static/img/img_now.jpg", cv_bandpass)
