import streamlit as st
import pickle
import pandas as pd
import requests

# number of movies
THRESHOLD = 5

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8742f8f521437ef36794cbcf3946309c'.format(movie_id))
    data = response.json()
    # st.text('https://api.themoviedb.org/3/movie/{}?api_key=8742f8f521437ef36794cbcf3946309c'.format(movie_id))
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:THRESHOLD+1]

    recommended_movies = []
    recommended_movies_poster = []

    # from movies_list we take out movie name and add in recommended_movies variable, then add poster
    # from fetch_poster() function and add in recommended_movies_posters and we return both posters, movies

    for i in movies_list:
        
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        flag = True

        while flag:
            try:
                q = fetch_poster(movie_id)
                # print(q)
                # print(type(q))
                recommended_movies_poster.append(q)
                flag = False
            except:
                pass
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Choose your movie',
 movies['title'].values)

# Hide the output of JSON strings
st.set_option('deprecation.showfileUploaderEncoding', False)

if st.button('Recommend similar movies'):
    names, posters = recommend(selected_movie_name)
    print(names)

    for col, nm, pst in zip(st.columns(THRESHOLD), names, posters):
        with col:
            st.text(nm)
            st.image(pst)

st.markdown("~ ***Geetika Kanwar*** ")

