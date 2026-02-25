import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("movies.csv")

# Select required columns (based on YOUR dataset)
movies = movies[['original_title', 'overview', 'genres']]
movies.dropna(inplace=True)

# Rename column for simplicity
movies.rename(columns={'original_title': 'title'}, inplace=True)

# Combine text features
movies['content'] = movies['overview'] + " " + movies['genres']

# Convert text to numerical vectors
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['content'])

# Compute cosine similarity
similarity = cosine_similarity(tfidf_matrix)

# Recommendation function
def recommend(movie_name):
    index = movies[movies['title'] == movie_name].index[0]
    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    return [movies.iloc[i[0]].title for i in scores]

# Streamlit UI
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a Movie", movies['title'])

if st.button("Recommend"):
    st.subheader("Recommended Movies:")
    for movie in recommend(selected_movie):
        st.write(movie)