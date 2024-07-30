from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import logging

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MODEL_PATH = 'VGG19_Model.h5'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Attempt to load the model
try:
    model = load_model(MODEL_PATH)
    app.logger.info("Model loaded successfully.")
except Exception as e:
    app.logger.error(f"Error loading model: {e}")
    model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_prediction(image_path):
    if model is None:
        return "Model not loaded", 0.0

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (240, 240))
    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image)
    confidence = prediction.max() * 100
    result = "Yes" if prediction[0] > 0.5 else "No"
    return result, confidence

@app.route('/')
@app.route('/home')
def home():
    return render_template('main.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('result.html', prediction='No file uploaded')

    file = request.files['file']
    if not allowed_file(file.filename):
        return render_template('result.html', prediction='Invalid file type')

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    prediction, confidence = get_prediction(file_path)
    image_url = f'/upload/{filename}'

    return render_template('result.html', prediction=prediction, prediction_percentage=confidence, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
