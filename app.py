import pickle
import streamlit as st
import requests
import gdown
import os

# Function to download similarity.pkl if not available
def download_similarity_file():
    file_id = "1zvr1CPR657JNOiwc4hLR1xzj8ArHqVbv"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "similarity.pkl"
    
    if not os.path.exists(output):
        st.info("Downloading similarity.pkl...")
        gdown.download(url, output, quiet=False)
        st.success("Download complete!")

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    
    return recommended_movie_names, recommended_movie_posters

# Download similarity.pkl if not available
download_similarity_file()

# Load movie data
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Custom styling
st.markdown("""
    <style>
        body {
            background-color: #1E1E1E;
            color: white;
        }
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #E50914;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #aaa;
        }
        .stSelectbox {
            width: 80%;
            margin: auto;
        }
        .movie-title {
            font-size: 16px;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title'>Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Find your next favorite movie</p>", unsafe_allow_html=True)

# Searchable dropdown
selected_movie = st.selectbox("Search or select a movie:", options=movies['title'].unique())

# Show recommendations on button click
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations in a grid layout
    st.write("### Recommended Movies")
    cols = st.columns(5)
    
    for i, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[i], use_container_width=True)  # Updated parameter
            st.markdown(f"<p class='movie-title'>{recommended_movie_names[i]}</p>", unsafe_allow_html=True)
