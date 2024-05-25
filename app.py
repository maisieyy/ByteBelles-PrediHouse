from flask import Flask, render_template, request
import pickle
import pandas as pd
import xgboost
from sklearn.metrics.pairwise import cosine_similarity

# Load the model
with open('xgb_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as j:
    scaler = pickle.load(j)

with open('X_normalized.pkl', 'rb') as k:
    normalized = pickle.load(k)

# Load dataset
original_data = pd.read_csv('data_rumah.csv')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", original_input=None, result=None, recommendations=[])

@app.route('/predict-area', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        lb = int(request.form['lb'])
        lt = int(request.form['lt'])
        kt = int(request.form['kt'])
        km = int(request.form['km'])
        input_variables = pd.DataFrame([[lb, lt, kt, km]], columns=['LB', 'LT', 'KT', 'KM'])
        prediction = model.predict(input_variables)[0]
        return render_template('index.html', original_input={'LB': lb, 'LT': lt, 'KT': kt, 'KM': km}, result=prediction, recommendations=[])
    return render_template('index.html', original_input=None, result=None, recommendations=[])

@app.route('/recommendations', methods=['POST'])
def recommendations():
    lb = int(request.form['lb'])
    lt = int(request.form['lt'])
    kt = int(request.form['kt'])
    km = int(request.form['km'])
    
    # Predict nilai harga
    input_variables_for_prediction = pd.DataFrame([[lb, lt, kt, km]], columns=['LB', 'LT', 'KT', 'KM'])
    harga = model.predict(input_variables_for_prediction)[0]
    
    # Pastikan kolom-kolom berada dalam urutan yang sama seperti saat pemasangan
    input_variables = pd.DataFrame([[harga, lb, lt, kt, km]], columns=['HARGA', 'LB', 'LT', 'KT', 'KM'])
    
    # Mengubah input menggunakan scaler yang sudah dipasang sebelumnya
    input_normalized = scaler.transform(input_variables)
    
    similarities = cosine_similarity(input_normalized, normalized)
    indices = similarities.argsort()[0][-6:][::-1]
    
    # Ambil rekomendasi aktual dari dataset asli
    recommendations = []
    for i in indices:
        rec = original_data.iloc[i]
        recommendations.append({
            "name": rec['NAMA RUMAH'],
            "price": rec['HARGA'],  
            "lb": rec['LB'],
            "lt": rec['LT'],
            "kt": rec['KT'],
            "km": rec['KM']
        })
    
    return render_template('index.html', recommendations=recommendations, original_input={'LB': lb, 'LT': lt, 'KT': kt, 'KM': km}, result=harga)

if __name__ == '__main__':
    app.run(debug=True)
