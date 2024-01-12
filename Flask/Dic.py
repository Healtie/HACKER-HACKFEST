from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
import base64

app = Flask(__name__)
CORS(app)

df = pd.read_csv('wd.csv')
df1 = df.iloc[:, 1:3].drop(0)
df1[['CALORIES', 'Sugar', 'Fat', 'Natrium']] = '-01'
df1 = df1.sort_values(by=['NAMA ITEM'])
df1['BARCODE'] = df1['BARCODE'].astype(str)

def find_barcode(barcode=''):
    df2 = df1.loc[df1['BARCODE'] == barcode]
    return df2

def classify_image(uri='https://i.ibb.co/TmjHfFq/image.png'):
    if not uri.startswith(('http://', 'https://')):
        return jsonify({'error': 'Invalid image URL'}), 400

    response = requests.get(uri)

    if response.status_code != 200:
        return jsonify({'error': 'Image not found'}), 404

    encoded_image = base64.b64encode(response.content).decode('utf-8')

    payload = {
        "requests": [
            {
                "features": [
                    {"maxResults": 40, "model": "builtin/latest", "type": "DOCUMENT_TEXT_DETECTION"},
                ],
                "image": {"content": encoded_image},
                "imageContext": {"cropHintsParams": {"aspectRatios": [0.8, 1, 1.2]}}
            }
        ]
    }

    response = requests.post('https://vision.googleapis.com/v1/images:annotate?key=AIzaSyCsFHX5pWsLd2FT3Zq-hkp8b5k8RuZgyiA', json=payload)

    if response.status_code != 200:
        return jsonify({'error': 'Document text detection failed'}), 500

    results = response.json().get('responses', [])
    document_text_detection_result = results[0].get('textAnnotations', [])

    if not document_text_detection_result:
        return jsonify({'error': 'No text found in image'}), 404

    delm = [' G', ' MG', ' ML', ' KKAL']
    newtext = document_text_detection_result[0]['description'].split('\n')
    poinvil = [newtext[idx-2:idx+3] for idx, word in enumerate(newtext) if any(keyword in word.upper() for keyword in delm)]

    if not poinvil:
        return jsonify({'error': 'No nutrition information found in text'}), 404

    df = pd.DataFrame(poinvil, columns=['Item1', 'Item2', 'Item3', 'Item4', 'Item5'])
    return df

@app.route('/get_data', methods=['GET'])
def get_data():
    return df1.to_json(orient='records')

@app.route('/find_barcode', methods=['GET'])
def get_barcode_info():
    barcode = request.args.get('barcode', default='', type=str)
    result_df = find_barcode(barcode)

    if result_df.empty:
        return jsonify({'error': 'Barcode not found'}), 404

    new_res = {
        'nama_item': result_df['NAMA ITEM'].values[0],
        'barcode': result_df['BARCODE'].values[0],
        'calories': result_df['CALORIES'].values[0],
        'sugar': result_df['Sugar'].values[0],
        'fat': result_df['Fat'].values[0],
        'natrium': result_df['Natrium'].values[0],
    }

    if '-01' in new_res.values():
        new_res['tindakan'] = 'EDIT HIDUP SEHAT ITU PENTING!'
    else:
        new_res['tindakan'] = 'BROO HIDUP SEHAT ITU PENTING!'

    return jsonify(new_res)

@app.route('/classify_image', methods=['GET'])
def classify_image_endpoint():
    uri = request.args.get('uri', default='', type=str)
    df = classify_image(uri)

    if isinstance(df, pd.DataFrame) and df.empty:
        return jsonify({'error': 'Nutrition information not found'}), 404

    important_data = {
        'protein': df['protein.value'][0],
        'calories': df['calories.value'][0],
        'fat': df['fat.value'][0],
        'carbs': df['carbs.value'][0],
    }

    return jsonify(important_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
