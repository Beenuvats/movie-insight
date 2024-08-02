import pandas as pd
import pickle
import streamlit as st

# Load movie info with IMDb IDs and poster URLs
movie_info_df = pd.read_csv('movie_info.csv')

# Load your movie similarity matrix
movies = pickle.load(open('C:/Users/NEERAJ SHARMA/1/movie_list.pkl', 'rb'))
similarity = pickle.load(open('C:/Users/NEERAJ SHARMA/1/similarity_2.pkl', 'rb'))

def get_movie_info_from_df(title):
    """Get IMDb ID and poster URL from DataFrame."""
    row = movie_info_df[movie_info_df['title'] == title]
    if not row.empty:
        imdb_id = row['imdb_id'].values[0]
        poster_url = row['poster_url'].values[0]
        return imdb_id, poster_url
    return 'N/A', 'No poster available'

def recommend(movie, movies, similarity):
    if movie not in movies['title'].values:
        return [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in range(1, min(6, len(distances))):
        idx = distances[i][0]
        recommended_movie_names.append(movies.iloc[idx]['title'])
        _, poster_url = get_movie_info_from_df(movies.iloc[idx]['title'])
        recommended_movie_posters.append(poster_url)

    return recommended_movie_names, recommended_movie_posters

# Streamlit app setup
st.set_page_config(page_title="Movie Recommender System", layout="wide")

st.header('Movie Recommender System')

# Movie selection
selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].tolist())

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)

    # Display recommendations
    if recommended_movie_names:
        cols = st.columns(len(recommended_movie_names))
        for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
            with cols[i]:
                st.text(name)
                if poster.startswith("http"):
                    st.image(poster)
                else:
                    st.write(poster)
    else:
        st.write("No recommendations found.")