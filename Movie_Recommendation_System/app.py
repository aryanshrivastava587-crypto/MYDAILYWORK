import os
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Get correct path for CSV (works locally + on Streamlit Cloud)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "movies.csv")

# Load dataset
movies = pd.read_csv(csv_path)

# Select required columns
movies = movies[['original_title', 'overview', 'genres']]
movies.dropna(inplace=True)

# Rename column
movies.rename(columns={'original_title': 'title'}, inplace=True)

# Combine text features
movies['content'] = movies['overview'] + " " + movies['genres']

# Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['content'])

# Similarity calculation
similarity = cosine_similarity(tfidf_matrix)

# Recommendation function
def recommend(movie_name):
    index = movies[movies['title'] == movie_name].index[0]
    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    return [movies.iloc[i[0]].title for i in scores]

# UI
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a Movie", movies['title'])

if st.button("Recommend"):
    st.subheader("Recommended Movies:")
    for movie in recommend(selected_movie):
        st.write(movie)
