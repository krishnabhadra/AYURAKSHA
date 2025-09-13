from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Medicine API endpoint
@app.route('/get_medicine', methods=['POST'])
def get_medicine():
    drug_name = request.form.get('drug_name', '').strip()
    
    # OpenFDA API call
    url = f'https://api.fda.gov/drug/label.json?search=openfda.brand_name:"{drug_name}"&limit=1'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        try:
            result = data['results'][0]
            info = {
                'Uses': result.get('indications_and_usage', ['Not available'])[0],
                'Dosage': result.get('dosage_and_administration', ['Not available'])[0],
                'Side_Effects': result.get('adverse_reactions', ['Not available'])[0]
            }
            return jsonify(info)
        except (IndexError, KeyError):
            return jsonify({'error': 'Medicine not found'})
    else:
        return jsonify({'error': 'API error'})

if __name__ == "__main__":
    app.run(debug=True)
