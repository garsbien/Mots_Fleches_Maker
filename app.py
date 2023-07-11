import os
from flask import Flask, render_template, request, redirect, url_for, flash
from PIL import Image
from tkinter import filedialog
import pytesseract 
import cv2
import PyPDF2
import tkinter as tk

nb_lignes = 24  # Définition de la valeur de nb_lignes
nb_colonnes = 19 # Définition de la valeur de nb_colonnes
window = tk.Tk()  # Définition de la variable window
grid_frame = tk.Frame(window)  # Définition de la variable grid_frame
text_entries = [[None for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
text_entries = [[None for _ in range(nb_colonnes)] for _ in range(nb_lignes)]





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

def load_image_file(file_path):
    try:
        image = Image.open(file_path)
        # Traitez l'image ici (extraire les informations de la grille)
        # et mettez à jour l'interface utilisateur avec la grille chargée
    except IOError:
        print("Impossible de charger le fichier image")

def load_pdf_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            # Traitez le fichier PDF ici (extraire les informations de la grille)
            # et mettez à jour l'interface utilisateur avec la grille chargée
    except PyPDF2.PdfReadError:
        print("Impossible de charger le fichier PDF")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.png"), ("PDF Files", "*.pdf")])
    if file_path:
        if file_path.endswith('.pdf'):
            load_pdf_file(file_path)
        else:
            load_image_file(file_path)

def create_text_entries():
    for row in range(nb_lignes):
        for col in range(nb_colonnes):
            entry = tk.Entry(grid_frame, width=2)
            entry.grid(row=row, column=col)
            # Ajouter les cases de texte à une liste ou une structure de données appropriée
            # pour pouvoir y accéder et les mettre à jour ultérieurement
            text_entries[row][col] = entry

def get_user_letters():
    letters = []
    for row in range(nb_lignes):
        row_letters = []
        for col in range(nb_colonnes):
            entry = text_entries[row][col]
            letter = entry.get().upper()  # Convertir en majuscules
            row_letters.append(letter)
        letters.append(row_letters)
    return letters

def solve_grid():
    # Obtenir les lettres saisies par l'utilisateur
    user_letters = get_user_letters()
    # Utiliser les lettres saisies pour résoudre la grille      

def create_text_entries():
    # Le contenu de la fonction ici


 
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




