import os
from flask import Flask, render_template, request, redirect, url_for, flash
from PIL import Image
import pytesseract 
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}

# Configuration de Pytesseract pour l'OCR
pytesseract.pytesseract.tesseract_cmd = r'<"C:\Program Files\Tesseract-OCR\tesseract.exe">'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_letters_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return pytesseract.image_to_string(threshold, config='--psm 6')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            letters = extract_letters_from_image(os.path.join(UPLOAD_FOLDER, filename))
            # Effectuez ici le traitement des lettres extraites de l'image
            return render_template('result.html', letters=letters)
        else:
            flash('Invalid file format')
            return redirect(request.url)
    return render_template('index.html')


