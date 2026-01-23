import streamlit as st
import pickle
import pandas as pd
import requests
import gzip

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #121212;
    color: #ffffff;
}

h1 {
    text-align: center;
    color: #e50914;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #b3b3b3;
    font-size: 15px;
    margin-bottom: 30px;
}

div[data-baseweb="select"] > div {
    background-color: #1f1f1f;
    border-radius: 6px;
    min-height: 42px;
    color: white;
}

.stButton > button {
    background-color: #e50914;
    color: white;
    border-radius: 6px;
    padding: 8px 18px;
    font-size: 14px;
    font-weight: 600;
    border: none;
    display: block;
    margin: 15px auto 0 auto;
    width: 180px;
}

.stButton > button:hover {
    background-color: #f6121d;
}

.movie-card {
    background-color: #1f1f1f;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
}

.movie-title {
    font-size: 16px;
    font-weight: 600;
    margin-top: 10px;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

TMDB_API_KEY = st.secrets["tmdb_api_key"]
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
FALLBACK_POSTER = "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get("poster_path")
    if poster_path:
        return POSTER_BASE_URL + poster_path
    return FALLBACK_POSTER

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    names = []
    posters = []
    for i in movies_list:
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return names, posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

st.markdown("<h1>tamimystic Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Select a movie to get similar recommendations</div>", unsafe_allow_html=True)

center = st.columns([1, 2, 1])[1]

with center:
    selected_movie = st.selectbox(
        "Select a Movie",
        movies['title'].values
    )
    recommend_btn = st.button("Recommend Movies")

if recommend_btn:
    with st.spinner("Loading recommendations..."):
        names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
