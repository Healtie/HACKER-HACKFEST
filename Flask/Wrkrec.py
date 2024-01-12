import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model_and_recommend(dataset_path, input_calories):
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

# Contoh penggunaan fungsi
dataset_path = "set.csv"
input_calories = 2200

result = train_model_and_recommend(dataset_path, input_calories)
print(f"Rekomendasi Olahraga untuk {input_calories} kalori: {result}")
