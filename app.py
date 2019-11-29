import pytesseract as pt
from PIL import Image
import time
import datetime
import os
import urllib.request
from flask import Flask, request, redirect, jsonify, render_template
from werkzeug.utils import secure_filename
# pt.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
#pt.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'

# import our OCR function


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    img = Image.open(filename)
    # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    text = pt.image_to_string(img)
    return text


# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
# UPLOAD_FOLDER = 'C:\Users\BUCHI\Documents\HNGIntership\HNG6\Task 8 scrape\gabby\OCRi\uplo'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# route and function to handle the upload page
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template("upload.html")


@app.route('/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        # resp = jsonify({'message' : 'No file part in the request'})
        # resp.status_code = 400
        # return resp
        msg = 'No file part in the request'
        return render_template("upload.html", msg=msg)
    file = request.files['file']
    if file.filename == '':
        # resp = jsonify({'message' : 'No file selected for OCR'})
        # resp.status_code = 400
        # return resp
        msg = 'No file selected'
        return render_template("upload.html", msg=msg)
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1]
        timestr = time.strftime("%Y%m%d-%H%M%S")
        today = datetime.date.today()
        todaystr = today.isoformat()
        nam = timestr + "." + ext
        filename = secure_filename(nam)
        try:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], todaystr))
        except:
            pass
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], todaystr, filename))
        names = "static/" + todaystr + "/" + filename
        print(names)
        extracted_text = ocr_core(file)
        if extracted_text == '':
            extracted_text = "Sorry characters could not be clearly recognized"
            # resp = jsonify({'message' : extracted_text})
            # resp.status_code = 400
            # return resp
            return render_template("upload.html", extracted_text=extracted_text)
        # resp = jsonify({'message' : 'File successfully uploaded'})
        # resp = jsonify({'extracted_text' : extracted_text})
        # resp.status_code = 200
        # return resp
        return render_template("upload.html", extracted_text=extracted_text, img_src=names)
    else:
        # resp = jsonify({'message' : 'Allowed file types are png, jpg, jpeg'})
        # resp.status_code = 400
        # return resp
        msg = 'Allowed file types are png, jpg, jpeg'
        return render_template("upload.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
