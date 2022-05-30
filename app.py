import streamlit as slt
import pandas as pd
import requests
import pickle


slt.title('Movie Recommender System')

movies = pickle.load(open('movies.pkl','rb'))
movie_dict=pd.DataFrame(movies)

option = slt.selectbox('Choose a movie',movie_dict['title'].values)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ec804bb9fa4ff992884cd015d463dcf6&language=en-US'.format(movie_id))
    poster = response.json()
    return "https://image.tmdb.org/t/p/w500/" + poster['poster_path']

#def fetch_trailer(movie_id):
 #   response1=requests.get('https://api.themoviedb.org/3/movie/{}/videos?api_key=ec804bb9fa4ff992884cd015d463dcf6&language=en-US'.format(movie_id))
 #   vid = response1.json()
  #  final_trailer="https://www.youtube.com/watch?v=" + vid


def recommend(movies):
    fetch_index = movie_dict[movie_dict['title'] == movies].index[0]
    distance = similarity[fetch_index]
    final_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended=[]
    recommended_movie_posters = []
   # recommended_movie_trailers = []
    for i in final_list:

        movie_id=movie_id = movie_dict.iloc[i[0]].movie_id
        recommended.append(movie_dict.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        #recommended_movie_trailers.append(fetch_trailer(movie_id))
    return recommended , recommended_movie_posters

similarity=pickle.load(open('similarity.pkl','rb'))

if slt.button('Recommend') :
    recommended,recommended_movie_posters = recommend(option)
    col1, col2, col3, col4, col5 = slt.columns(5)

    with col1:
        slt.text(recommended[0])
        slt.image(recommended_movie_posters[0])
        #slt.text(recommended_movie_trailers[0])


    with col2:
        slt.text(recommended[1])
        slt.image(recommended_movie_posters[1])
        #slt.text(recommended_movie_trailers[1])


    with col3:
        slt.text(recommended[2])
        slt.image(recommended_movie_posters[2])
        #slt.text(recommended_movie_trailers[2])

    with col4:
        slt.text(recommended[3])
        slt.image(recommended_movie_posters[3])
        #slt.text(recommended_movie_trailers[3])

    with col5:
        slt.text(recommended[4])
        slt.image(recommended_movie_posters[4])
        #slt.text(recommended_movie_trailers[4])
