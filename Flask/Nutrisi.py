from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
import base64

app = Flask(__name__)
CORS(app)


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
        newres['tindakan'] = 'BROO HIDUP SEHAT ITU PENTING!'

    return jsonify(newres)

# http://34.171.82.75/classify_image?uri=custem.jpg
@app.route('/classify_image', methods=['GET'])
def classify_image():
    uri = request.args.get('uri', default='', type=str)

    # Cek apakah uri tidak kosong dan berisi URL gambar
    if not uri.startswith(('http://', 'https://')):
        return jsonify({'error': 'Invalid image URL'}), 400

    print('--------------')
    print(uri)
    print('--------------')

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
        # Tambahkan data lainnya yang dianggap penting di sini
    }

    # Kembalikan data dalam format JSON
    return jsonify(important_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)