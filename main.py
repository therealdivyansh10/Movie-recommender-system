import bz2

import streamlit as st
import pickle
import _pickle as cPickle
import pandas as pd
# import sklearn
import requests

movies = pickle.load(open("movies.pkl", "rb"))
movies_list = movies["title"].values


def fetch_poster(movie_id):
    key = "b720ec39d36849305a8963b680357ebd"
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id , key))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key= lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies,recommend_movies_poster


def decompress_pickle(file):
    data = bz2.BZ2File(file, "rb")
    data = cPickle.load(data)
    return data


similarity = decompress_pickle('similarity.pbz2')

# similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie recommendation system")
selected_option = st.selectbox("Select Your Movie", movies_list)

if st.button("Recommend"):
    names, posters = recommend(selected_option)
    col1, col2, col3 ,col4 , col5 =  st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])
    with col3:
        st.header(names[2])
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])
