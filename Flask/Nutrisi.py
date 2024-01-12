from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import requests
import base64

app = Flask(__name__)
CORS(app)

def train_and_recommend(dataset_path, input_calories):
    # Membaca dataset
    data = pd.read_csv(dataset_path)

    # Pisahkan fitur (X) dan target (y)
    X = data[['Kalori', 'Normal_Kalori']]
    y = data['Rekomendasi_Olahraga']

    # Membagi dataset menjadi data latih dan data uji
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Membuat model RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Melatih model
    model.fit(X_train, y_train)

    # Memprediksi data uji
    y_pred = model.predict(X_test)

    # Mengukur akurasi model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Akurasi Model: {accuracy * 100:.2f}%")

    # Fungsi untuk mendapatkan rekomendasi olahraga berdasarkan input kalori
    def get_recommendation(calories):
        input_data = pd.DataFrame({'Kalori': [calories], 'Normal_Kalori': [calories - 200]})
        recommendation = model.predict(input_data)
        return recommendation[0]

    # Mendapatkan rekomendasi olahraga
    recommended_sport = get_recommendation(input_calories)
    return recommended_sport

def barcodereadepoin():
    df = pd.read_csv('wd.csv')
    df1 = df.iloc[:, 1:3].drop(0)
    df1[['CALORIES', 'Sugar', 'Fat', 'Natrium']] = '-01'
    df1 = df1.sort_values(by=['NAMA ITEM'])
    df1['BARCODE'] = df1['BARCODE'].astype(str)
    return df1

def findbarcode(dfl, barcode=''):
    df2 = dfl.loc[dfl['BARCODE'] == barcode]
    return df2

def repoinforimgcal(api_key='2f154257cc40492d85643234db243009', poin='analyze', imgpoin='kosong'):
    url = f"https://api.spoonacular.com/food/images/{poin}"
    params = {
        "imageUrl": imgpoin,
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    rep = pd.DataFrame()

    if response.status_code == 200:
        data = response.json()
        rep = pd.json_normalize(data['nutrition'])
    else:
        rep = pd.DataFrame(
            {"error_message": f"Gagal mendapatkan respons. Kode status: {response.status_code}"}, index=[0])
    return rep

def textmanureader(api_key='AIzaSyCsFHX5pWsLd2FT3Zq-hkp8b5k8RuZgyiA', image_url='https://i.ibb.co/TmjHfFq/image.png'):
    url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key}'
    response = requests.get(image_url)
    encoded_image = base64.b64encode(response.content).decode('utf-8')

    payload = {
        "requests": [
            {
                "features": [
                    {"maxResults": 40, "model": "builtin/latest",
                        "type": "DOCUMENT_TEXT_DETECTION"},
                ],
                "image": {
                    "content": encoded_image
                },
                "imageContext": {
                    "cropHintsParams": {
                        "aspectRatios": [0.8, 1, 1.2]
                    }
                }
            }
        ]
    }

    response = requests.post(url, json=payload)
    results = response.json().get('responses', [])
    document_text_detection_result = results[0].get('textAnnotations', [])

    if document_text_detection_result:
        delm = [' G', ' MG', ' ML', ' KKAL']
        newtext = document_text_detection_result[0]['description'].split('\n')
        poinvil = [newtext[idx-2:idx+3] for idx, word in enumerate(
            newtext) if any(keyword in word.upper() for keyword in delm)]
    else:
        print("Tidak ada hasil DOCUMENT_TEXT_DETECTION.")
        poinvil = []

    df = pd.DataFrame(poinvil, columns=[
                      'Item1', 'Item2', 'Item3', 'Item4', 'Item5'])
    return df

dfl = barcodereadepoin()

@app.route('/get_data', methods=['GET'])
def get_data():
    return dfl.to_json(orient='records')

@app.route('/find_barcode', methods=['GET'])
def get_barcode():
    barcode = request.args.get('barcode', default='', type=str)
    result_df = findbarcode(dfl, barcode)

    newres = {
        'nama_item': result_df['NAMA ITEM'].values[0],
        'barcode': result_df['BARCODE'].values[0],
        'calories': result_df['CALORIES'].values[0],
        'sugar': result_df['Sugar'].values[0],
        'fat': result_df['Fat'].values[0],
        'natrium': result_df['Natrium'].values[0],
    }

    if '-01' in newres.values():
        newres['tindakan'] = 'EDIT HIDUP SEHAT ITU PENTING!'
    else:
        newres['tindakan'] = 'HIDUP SEHAT ITU PENTING!'

    return jsonify(newres)

# http://34.171.82.75/classify_image?uri=custem.jpg
@app.route('/classify_image', methods=['GET'])
def classify_image():
    uri = request.args.get('uri', default='', type=str)

    # Cek apakah uri tidak kosong dan berisi URL gambar
    if not uri.startswith(('http://', 'https://')):
        return jsonify({'error': 'Invalid image URL'}), 400

    # Panggil fungsi repoinforimgcal dengan uri sebagai parameter
    repwo = repoinforimgcal(imgpoin=uri)

    # Cek apakah repwo adalah objek DataFrame
    if not isinstance(repwo, pd.DataFrame):
        return jsonify({'error': 'Failed to classify image'}), 500

    # Ambil data yang penting dan simpan dalam variabel array baru
    important_data = {
        'protein': repwo['protein.value'][0],
        'calories': repwo['calories.value'][0],
        'fat': repwo['fat.value'][0],
        'carbs': repwo['carbs.value'][0],
    }

    # Kembalikan data dalam format JSON
    return jsonify(important_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
