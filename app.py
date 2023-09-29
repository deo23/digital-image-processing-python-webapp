import numpy as np
from PIL import Image
import image_processing
import os
from flask import Flask, render_template, request, make_response, current_app
from datetime import datetime
from functools import wraps, update_wrapper
from shutil import copyfile
import threading
import random

app = Flask(__name__, static_folder="static")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Lock to ensure only one image processing operation at a time
image_processing_lock = threading.Lock()


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Last-Modified"] = datetime.now()
        response.headers[
            "Cache-Control"
        ] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return update_wrapper(no_cache, view)


# Define a function to process images asynchronously
def process_image_async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with image_processing_lock:
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()
            thread.join()  # Wait for the image processing thread to complete

            # Perform actions that require access to the main thread here
            # Use current_app and request objects to ensure access to the main thread context
            with current_app.app_context():
                current_app.logger.info(
                    "Image processing completed."
                )  # Example log message

                if request:
                    request.session[
                        "image_processed"
                    ] = True  # Example of updating the request context

        return "Processing image... Please wait."

    return wrapper


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("home.html", file_path="img/image_here.jpg")


@app.route("/about")
@nocache
def about():
    return render_template("about.html")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


@app.route("/upload", methods=["POST"])
@nocache
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    if not os.path.isdir(target):
        if os.name == "nt":
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/normal", methods=["POST"])
@nocache
def normal():
    copyfile("static/img/img_normal.jpg", "static/img/img_now.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/grayscale", methods=["POST"])
@nocache
def grayscale():
    image_processing.grayscale()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    image_processing.zoomin()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    image_processing.zoomout()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_left", methods=["POST"])
@nocache
def move_left():
    image_processing.move_left()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_right", methods=["POST"])
@nocache
def move_right():
    image_processing.move_right()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_up", methods=["POST"])
@nocache
def move_up():
    image_processing.move_up()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_down", methods=["POST"])
@nocache
def move_down():
    image_processing.move_down()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_addition", methods=["POST"])
@nocache
def brightness_addition():
    image_processing.brightness_addition()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_substraction", methods=["POST"])
@nocache
def brightness_substraction():
    image_processing.brightness_substraction()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_multiplication", methods=["POST"])
@nocache
def brightness_multiplication():
    image_processing.brightness_multiplication()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_division", methods=["POST"])
@nocache
def brightness_division():
    image_processing.brightness_division()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_equalizer", methods=["POST"])
@nocache
def histogram_equalizer():
    image_processing.histogram_equalizer()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/edge_detection", methods=["POST"])
@nocache
def edge_detection():
    image_processing.edge_detection()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/blur", methods=["POST"])
@nocache
def blur():
    image_processing.blur()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/sharpening", methods=["POST"])
@nocache
def sharpening():
    image_processing.sharpening()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_rgb", methods=["POST"])
@nocache
def histogram_rgb():
    image_processing.histogram_rgb()
    if image_processing.is_grey_scale("static/img/img_now.jpg"):
        return render_template("histogram.html", file_paths=["img/grey_histogram.jpg"])
    else:
        return render_template(
            "histogram.html",
            file_paths=[
                "img/red_histogram.jpg",
                "img/green_histogram.jpg",
                "img/blue_histogram.jpg",
            ],
        )


@app.route("/thresholding", methods=["POST"])
@nocache
def thresholding():
    lower_thres = int(request.form["lower_thres"])
    upper_thres = int(request.form["upper_thres"])
    image_processing.threshold(lower_thres, upper_thres)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/average_blur", methods=["POST"])
@nocache
def average_blur():
    image_processing.average_blur()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/median_blur", methods=["POST"])
@nocache
def median_blur():
    ksize = int(request.form["median-blur"])
    image_processing.median_blur(ksize)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/gaussian_blur", methods=["POST"])
@nocache
def gaussian_blur():
    ksize = int(request.form["gaussian-blur"])
    image_processing.gaussian_blur(ksize)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/bilateral_filter", methods=["POST"])
@nocache
def bilateral_filter():
    image_processing.bilateral_filter()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zero_padding", methods=["POST"])
@nocache
def zero_padding():
    image_processing.zero_padding()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/lowpass_filter", methods=["POST"])
@nocache
def lowpass_filter():
    size = int(request.form["lowpass-filter"])
    image_processing.lowpass_filter(size)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/highpass_filter", methods=["POST"])
@nocache
def highpass_filter():
    size = int(request.form["highpass-filter"])
    image_processing.highpass_filter(size)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/bandpass_filter", methods=["POST"])
@nocache
def bandpass_filter():
    size = int(request.form["bandpass-filter"])
    image_processing.bandpass_filter(size)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
