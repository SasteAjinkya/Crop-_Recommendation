from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
from model import CropModel
import pandas as pd
from datetime import datetime

app = Flask(__name__)
model = CropModel()
model.load_model('crop_model.pkl', 'scaler.pkl')


EXCEL_FILE_PATH = 'Input_Data.xlsx'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = [
        float(data['N']),
        float(data['P']),
        float(data['K']),
        float(data['humidity']),
        float(data['ph']),
        float(data['rainfall']),
        float(data['temperature'])
    ]
    prediction = model.predict(features)
    predicted_crop = prediction[0]
    region = data['region']  

    
    input_data = {
        'N': data['N'],
        'P': data['P'],
        'K': data['K'],
        'Humidity': data['humidity'],
        'Soil pH': data['ph'],
        'Rainfall': data['rainfall'],
        'Temperature': data['temperature'],
        'Region': region,  
        'Predicted Crop': predicted_crop,
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    
    df = pd.DataFrame([input_data])
    
    
    try:
        
        existing_data = pd.read_excel(EXCEL_FILE_PATH)
        df = pd.concat([existing_data, df], ignore_index=True)
        df.to_excel(EXCEL_FILE_PATH, index=False)
    except FileNotFoundError:
        
        df.to_excel(EXCEL_FILE_PATH, index=False)

    
    return jsonify({'predicted_crop': predicted_crop, 'region': region})


@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('images', filename)


@app.route('/region_recommendations', methods=['GET'])
def region_recommendations():
    region = request.args.get('region')  
    if region:
        
        data = pd.read_excel(EXCEL_FILE_PATH)
        region_data = data[data['Region'] == region]

        
        recommended_crops = region_data['Predicted Crop'].value_counts().index.tolist()

        return jsonify({'region': region, 'recommended_crops': recommended_crops})
    else:
        return jsonify({'error': 'Region not specified'})
    
@app.route('/reports')
def reports():
        return render_template('reports.html')




@app.route('/viewdata', methods=['GET', 'POST'])
def view_data():
    
    try:
        data = pd.read_excel(EXCEL_FILE_PATH)
    except FileNotFoundError:
        data = pd.DataFrame()

    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'delete':
            
            row_index = int(request.form['row_index'])
            data = data.drop(index=row_index)
            data.to_excel(EXCEL_FILE_PATH, index=False)

        return redirect(url_for('view_data'))  

    
    return render_template('viewdata.html', data=data.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
