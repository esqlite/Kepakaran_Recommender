from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# Load dataset
pakar_df = pd.read_excel('datasets/pakar.xlsx')

# Debugging: Print kolom dan beberapa baris awal untuk memastikan data benar
print(pakar_df.columns)  # Melihat daftar kolom yang tersedia
print(pakar_df.head())   # Menampilkan beberapa baris pertama dataset

# Isi nilai kosong pada kolom 'nama' dengan 'Unknown Expert' untuk menghindari error
pakar_df['name'] = pakar_df['name'].fillna('Unknown Expert')

# TF-IDF and cosine similarity
vectorizer = TfidfVectorizer(stop_words='english')
# Using the 'pakar' column for analysis
tfidf_matrix = vectorizer.fit_transform(pakar_df['pakar'].fillna(''))
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# KNN setup
knn = NearestNeighbors(n_neighbors=6, metric='cosine')
knn.fit(tfidf_matrix)

# Flask App
app = Flask(__name__)

# Function to find the index of the most similar experts
def recommend_experts(keyword, top_n=5):
    keyword_tfidf = vectorizer.transform([keyword])
    distances, indices = knn.kneighbors(keyword_tfidf, n_neighbors=top_n + 1)

    recommendations = []
    for i in range(1, len(indices[0])):  # Skip the first result (the query itself)
        idx = indices[0][i]
        expert = pakar_df.iloc[idx]
        recommendations.append({
            'name': expert['name'],  # Pastikan 'name' sesuai dengan nama kolom di dataset
            'image': expert['image'],
            'jenjang': expert['jenjang'],
            'h_index': expert['h_index'],
            'scopus': expert['scopus'],
            'pakar': expert['pakar']
        })
    return recommendations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    pakar_query = request.form['pakar_query']
    num_recommendations = int(request.form.get('num_recommendations', 4))  # Default to 4 recommendations

    recommendations = recommend_experts(pakar_query, top_n=num_recommendations)

    if not recommendations:
        return render_template('index.html', error="No experts found for the given keyword.")

    return render_template('recommendations.html', pakar_query=pakar_query, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
