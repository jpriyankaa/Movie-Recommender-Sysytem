import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()

    # tmdb image path + poster path = complete poster path
    return "https://image.tmdb.org/t/p/original" + data ['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

# Custom CSS
st.markdown ("""
<style>
body {
    background-color: #e6e6fa;
}
.main {
    background-color: #f0fff0;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
h1 {
    color: #000080;
    text-align: center;
}

h2, h3, h4, h5, h6 {
    color: #000080; 
}

.stButton button {
    background-color: #0073e6;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
}
.stButton button:hover {
    background-color: #004d00;
}

.custom-text {
    font-size: 15px; /* Increase text size */
    font-weight: bolder; /* Make text bold */
}
</style>
""", unsafe_allow_html=True)

st.title('Movie Recommender system')

selected_movie_name = st.selectbox(
    "Search for movies", movies['title'].values)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f'<p class="custom-text">{names[0]}</p>', unsafe_allow_html=True)
        st.image(posters[0])

    with col2:
        st.markdown(f'<p class="custom-text">{names[1]}</p>', unsafe_allow_html=True)
        st.image(posters[1])

    with col3:
        st.markdown(f'<p class="custom-text">{names[2]}</p>', unsafe_allow_html=True)
        st.image(posters[2])

    with col4:
        st.markdown(f'<p class="custom-text">{names[3]}</p>', unsafe_allow_html=True)
        st.image(posters[3])

    with col5:
        st.markdown(f'<p class="custom-text">{names[4]}</p>', unsafe_allow_html=True)
        st.image(posters[4])