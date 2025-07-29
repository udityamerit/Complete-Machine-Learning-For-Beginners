from flask import Flask, render_template, request
import pickle
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load models
ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))

def create_risk_chart(prediction):
    plt.figure(figsize=(8, 2))
    risk_levels = ['Low', 'Moderate', 'High']
    values = [10, 20, max(30, prediction+5)]  # Dynamic scale
    
    # Create gradient fill
    for i in range(len(values)-1):
        plt.fill_between([i, i+1], [0, 0], [1, 1], 
                        color=plt.cm.RdYlGn_r(i/3), alpha=0.3)
    
    plt.bar(2*(prediction/values[-1]), 1, width=0.2, color='#ff6b35')
    plt.text(2*(prediction/values[-1]), 1.1, f'FWI: {prediction}', 
            ha='center', fontsize=12, color='#ff6b35')
    
    plt.xticks(range(len(risk_levels)), risk_levels)
    plt.yticks([])
    plt.title('Fire Risk Assessment', pad=20)
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.read()).decode('ascii')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = {k: float(v) if k not in ['Classes', 'Region'] else v 
               for k, v in request.form.items()}
        
        # Encode categoricals (adjust mappings to match your training)
        cat_mapping = {
            'Classes': {'fire': 1, 'no fire': 0},
            'Region': {'north': 0, 'south': 1, 'east': 2, 'west': 3}
        }
        
        features = np.array([
            data['Temperature'],
            data['RH'],
            data['Ws'],
            data['Rain'],
            data['FFMC'],
            data['DMC'],
            data['ISI'],
            cat_mapping['Classes'].get(data['Classes'].lower(), 0),
            cat_mapping['Region'].get(data['Region'].lower(), 0)
        ]).reshape(1, -1)
        
        scaled_features = scaler.transform(features)
        prediction = round(float(ridge_model.predict(scaled_features)[0]), 2)
        
        # Create visualization
        chart_url = create_risk_chart(prediction)
        
        return render_template('result.html',
                            prediction=prediction,
                            input_data=data,
                            chart_url=chart_url)
    
    except Exception as e:
        return render_template('home.html', 
                             error=f"Error: {str(e)}. Please check your inputs.")

if __name__ == '__main__':
    app.run(debug=True)