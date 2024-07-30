from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
import numpy as np

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'upload')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'Brain_model_best.h5')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_prediction(image_path):
    model = load_model(MODEL_PATH)
    img = load_img(image_path, color_mode='grayscale', target_size=(224, 224))
    img = np.array(img) / 255.
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    prediction = prediction.argmax(axis=-1)
    return 'Healthy' if prediction == 1 else 'Affected'

def index(request):
    return render(request, 'main.html')

def predict(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if not allowed_file(file.name):
            return render(request, 'result.html', {'prediction': 'Invalid file type'})
        fs = FileSystemStorage(location=UPLOAD_FOLDER)
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)
        prediction = get_prediction(file_path)
        return render(request, 'result.html', {'prediction': prediction})
    return render(request, 'main.html')
