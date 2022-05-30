import numpy as np
import pandas as pd 
import csv


movies=pd.read_csv('tmdb_5000_movies.csv')
#movies.head(1)
credits=pd.read_csv('tmdb_5000_credits.csv')
#credits.head(1)

movies = movies.merge(credits,on='title')
#movies.head()
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.head(1)



movies.dropna(inplace=True)
movies.isnull().sum()

movies.duplicated().sum()
movies.head(1)

movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.head()

import ast
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 
movies['genres'] = movies['genres'].apply(convert)
movies.head()



movies['keywords'] = movies['keywords'].apply(convert)
movies.head()

def convert_2(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L 
movies['cast'] = movies['cast'].apply(convert_2)
movies.head()

def convert_3(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 
movies['crew'] = movies['crew'].apply(convert_3)
movies.head(1)

def remove_space(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1
movies['cast'] = movies['cast'].apply(remove_space)
movies['crew'] = movies['crew'].apply(remove_space)
movies['genres'] = movies['genres'].apply(remove_space)
movies['keywords'] = movies['keywords'].apply(remove_space)
movies.head(1)

movies['Mark'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies.head(1)


new_movies=movies[['movie_id','title','Mark']]
new_movies.head()


new_movies['Mark'] = movies['Mark'].apply(lambda x: " ".join(x))
new_movies.head(1)


new_movies['Mark'] = new_movies['Mark'].apply(lambda x:x.lower())
new_movies.head(1)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
    
vec = cv.fit_transform(new_movies['Mark']).toarray()

vec[1]

cv.get_feature_names()



import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()



def stemming(text):
  list2=[]
  for i in text.split():
    list2.append(ps.stem(i))
  return " ".join(list2)


new_movies['Mark']= new_movies['Mark'].apply(stemming)

new_movies['Mark']

vector1 = cv.fit_transform(new_movies['Mark']).toarray()
vector1[1]

cv.get_feature_names()

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector1)
similarity

def recommend(movie):
    fetch_index = new_movies[new_movies['title'] == movie].index[0]
    distance=similarity[fetch_index]
    final_list=sorted(list(enumerate(distance)),reverse=True,key = lambda x: x[1])[1:6]
    for i in final_list:
      print(new_movies.iloc[i[0]].title)




recommend('Batman')



new_movies['title'].values

import pickle

pickle.dump(new_movies.to_dict(),open('movies.pkl','wb'))

pickle.dump(similarity,open('similarity.pkl','wb'))
