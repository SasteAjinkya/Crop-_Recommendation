# model.py
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class CropModel:
    def __init__(self):
        self.model = None
        self.scaler = None

    def train(self, X, y):
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        self.model = RandomForestClassifier()
        self.model.fit(X_scaled, y)

    def predict(self, input_data):
        input_data = self.scaler.transform([input_data])
        return self.model.predict(input_data)

    def save_model(self, model_path, scaler_path):
        with open(model_path, 'wb') as model_file:
            pickle.dump(self.model, model_file)
        with open(scaler_path, 'wb') as scaler_file:
            pickle.dump(self.scaler, scaler_file)

    def load_model(self, model_path, scaler_path):
        with open(model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)
        with open(scaler_path, 'rb') as scaler_file:
            self.scaler = pickle.load(scaler_file)
