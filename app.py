from flask import Flask, request, render_template
import numpy as np
import pickle

app = Flask(__name__)

# Load the trained model
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        features = [
            float(request.form['ph']),
            float(request.form['Hardness']),
            float(request.form['Solids']),
            float(request.form['Chloramines']),
            float(request.form['Sulfate']),
            float(request.form['Conductivity']),
            float(request.form['Organic_carbon']),
            float(request.form['Trihalomethanes']),
            float(request.form['Turbidity'])
        ]
        
        # Convert to NumPy array for prediction
        input_data = np.array(features).reshape(1, -1)
        prediction = model.predict(input_data)
        
        # Interpret prediction
        if prediction[0] == 1:
            result = "The water is potable (safe to drink)."
        else:
            result = "The water is not potable (not safe to drink)."
            
        return render_template('index.html', result=result)
    
    except ValueError:
        return render_template('index.html', result="Invalid input! Please enter numeric values.")

if __name__ == "__main__":
    app.run(debug=True)



