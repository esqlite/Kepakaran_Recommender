from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import ast
from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import requests

# Load movie and credits data
movies = pd.read_csv('datasets/tmdb_5000_movies.csv')
credits = pd.read_csv('datasets/tmdb_5000_credits.csv')

# Preprocessing
credits = credits.rename(columns={'movie_id': 'id'})
movies = movies.merge(credits, on='id')
movies['genres'] = movies['genres'].fillna('')
movies['cast'] = movies['cast'].fillna('')
movies['genres'] = movies['genres'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)] if isinstance(x, str) else [])
movies['cast'] = movies['cast'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)] if isinstance(x, str) else [])
movies['combined_features'] = movies['genres'].apply(lambda x: ' '.join(x)) + ' ' + movies['cast'].apply(lambda x: ' '.join(x))
movies = movies.drop(columns=['title_y'])
movies = movies.rename(columns={'title_x': 'title'})

# Function to combine features into a single string
def combine_features(row):
    # Handle missing or non-string values by converting to string
    genres = " ".join(row['genres']) if isinstance(row['genres'], list) else str(row['genres'])
    keywords = " ".join(row['keywords']) if isinstance(row['keywords'], list) else str(row['keywords'])
    cast = " ".join(row['cast']) if isinstance(row['cast'], list) else str(row['cast'])
    overview = str(row['overview'])  # Ensure 'overview' is a string

    # Combine all features into a single string
    return genres + ' ' + keywords + ' ' + cast + ' ' + overview

# Apply the function to create the 'combined_features' column
movies['combined_features'] = movies.apply(combine_features, axis=1)

# Function to extract 'name' from a list of dictionaries
def extract_names(data):
    try:
        # If the data is a string representation of a list, convert it back to a list
        if isinstance(data, str):
            data = ast.literal_eval(data)
        
        # If it's a list of dictionaries, extract the 'name' field from each dictionary
        if isinstance(data, list):
            names = [item['name'] for item in data if isinstance(item, dict)]
            return " ".join(names)  # Join names with a space
        else:
            return ""  # Return empty string if it's not a valid list
    except:
        return ""  # Return empty string if an error occurs

# Function to combine features into a single string
def combine_features(row):
    # Extract the 'name' field for each feature (genres, keywords, cast)
    genres = extract_names(row['genres'])
    keywords = extract_names(row['keywords'])
    cast = extract_names(row['cast'])
    overview = str(row['overview'])  # Ensure 'overview' is a string
    
    # Combine all features into a single string
    return genres + ' ' + keywords + ' ' + cast + ' ' + overview

# Apply the function to create the 'combined_features' column
movies['combined_features'] = movies.apply(combine_features, axis=1)

def clean_keywords(keywords_str):
    # If the keyword string is empty or None, return an empty set
    if not keywords_str:
        return set()  # Return empty set if no keywords exist
    
    try:
        # Safely evaluate the string to convert it to a list of dictionaries
        keywords_list = ast.literal_eval(keywords_str)
    except:
        return set()  # Return empty set if evaluation fails
    
    # Extract 'name' field from each dictionary in the list (if it's a dictionary and has 'name' key)
    cleaned_keywords = [kw['name'] for kw in keywords_list if isinstance(kw, dict) and 'name' in kw]
    
    # Debugging: Print cleaned keywords
    #print(f"Cleaned keywords: {cleaned_keywords}")
    
    # Return a set of cleaned keywords
    return set(cleaned_keywords)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Image"
    return full_path

# TF-IDF and cosine similarity
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Use KNN to find the most similar movies based on TF-IDF features
knn = NearestNeighbors(n_neighbors=6, metric='cosine')
knn.fit(tfidf_matrix)

# Flask App
app = Flask(__name__)

# Fuzzy matching for titles
def get_movie_index(movie_title):
    best_match, score = process.extractOne(movie_title, movies['title'].values)
    if score < 70:
        return None
    return movies[movies['title'] == best_match].index[0]

def recommend_movies(movie_title, top_n=5):
    movie_index = get_movie_index(movie_title)
    if movie_index is None:
        return []

    # Fit KNN on the tf-idf matrix
    knn = NearestNeighbors(n_neighbors=top_n + 1, metric='cosine')
    knn.fit(tfidf_matrix)

    # Get nearest neighbors for the selected movie
    distances, indices = knn.kneighbors(tfidf_matrix[movie_index])

    recommendations = []
    for i in range(1, len(indices[0])):  # Skip the first movie (the input movie itself)
        similar_movie_index = indices[0][i]
        similar_movie_title = movies.iloc[similar_movie_index]['title']
        movie_id = movies.iloc[similar_movie_index]['id']
        poster_url = fetch_poster(movie_id)  # Fetch poster dynamically
        
        recommendations.append({
            'title': similar_movie_title,
            'poster': poster_url,
            'movie_title': similar_movie_title  # Add movie title to be passed to the front-end
        })

    return recommendations


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    num_recommendations = int(request.form.get('num_recommendations', 5))  # Default to 5 if not provided
    recommendations = recommend_movies(movie_title, top_n=num_recommendations)

    if not recommendations:
        return render_template('index.html', error="Movie not found or no recommendations.")

    return render_template('recommendations.html', movie_title=movie_title, recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)
