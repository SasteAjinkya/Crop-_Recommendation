# controller.py
import pandas as pd
from model import CropModel


data = pd.read_csv('data/Crop_recommendation.csv')


X = data[['N', 'P', 'K', 'humidity', 'ph', 'rainfall', 'temperature']]
y = data['label']


crop_model = CropModel()
crop_model.train(X, y)
crop_model.save_model('crop_model.pkl', 'scaler.pkl')
