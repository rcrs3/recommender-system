import pandas as pd
import numpy as np
import re
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import normalize
from sklearn.neighbors import KNeighborsRegressor

genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary',
                                       'Drama', 'Fantasy', 'Film-noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                                       'Thriller', 'War', 'Western']

def process():
    movies_info = pd.read_csv('data/raw/movies_list.csv')
    movies_info = movies_info.drop(['Website', 'BoxOffice'], axis = 1)
    movies_info_upd = movies_info[movies_info.Title != 'False'].reset_index().drop(['index', 'Response'], axis = 1)
    movies_info_upd = movies_info_upd[movies_info_upd.Plot.isnull() == False]
    movies_info_upd = movies_info_upd[movies_info_upd.Genre.isnull() == False]
    movies_info_upd = movies_info_upd[movies_info_upd.Actors.isnull() == False]
    movies_info_upd = movies_info_upd.drop_duplicates().reset_index().drop('index', axis = 1)
    movies_genre = pd.DataFrame(columns = ['Title', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary',
                                           'Drama', 'Fantasy', 'Film-noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                                           'Thriller', 'War', 'Western'])
    index = 0
    for row in movies_info_upd.itertuples(index = False):
        has_genre = []
        has_genre.append(row[0])
        genre_movie = row[5].split(',')
        index_aux = 0
        for j in range(len(genres)):
            has = False
            for k in range(index_aux, len(genre_movie)):
                if genres[j] == genre_movie[k]:
                    has_genre.append(1)
                    has = True
                    index_aux += 1
                    break
                        
            if(has == False):
                has_genre.append(0)
        movies_genre.loc[index] = has_genre
        index += 1
    movies_genre = movies_genre.drop_duplicates().reset_index().drop('index', axis = 1)
    movies_genre.loc[:, movies_genre.columns != 'Title'] = normalize(movies_genre.loc[:, movies_genre.columns != 'Title'], axis = 0)
    movies_info_final = pd.merge(movies_info_upd, movies_genre, on='Title')
    return movies_info_final


def tfidf(movies_info_final):
    tf_plot = TfidfVectorizer(analyzer = 'word', ngram_range = (1, 3), min_df = 0, stop_words = 'english')
    tf_actor = TfidfVectorizer(analyzer = 'word', ngram_range = (1, 3), min_df = 0, stop_words = 'english')
    tfidf_matrix_plot = tf_plot.fit_transform(movies_info_final['Plot'])
    tfidf_matrix_actor = tf_actor.fit_transform(movies_info_final['Actors'])

    cosine_similarities_plot = linear_kernel(tfidf_matrix_plot, tfidf_matrix_plot)
    cosine_similarities_genre = linear_kernel(movies_info_final[genres], movies_info_final[genres])
    cosine_similarities_actor = linear_kernel(tfidf_matrix_actor, tfidf_matrix_actor)
    cosine_similarities_total = (2*cosine_similarities_plot + 3*cosine_similarities_genre)/5
    return cosine_similarities_total
    
        
movies_info_final = process()
cosine_similarities_total = tfidf(movies_info_final)


def similar_movie(movies, movies_info_final, cosine_similarities_total):
    X = []
    y = []
    genre_mean = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    similar_indices = []
    movies_already_choosen = []
    for index, row in movies_info_final.iterrows():
        if(movies_info_final['Title'][index] in movies):
            similar_indices.append(cosine_similarities_total[index].argsort()[:-100:-1])
            new_genre_mean = list(movies_info_final.loc[index, genres])
            genre_mean = [g1 + g2 for g1, g2 in zip(genre_mean, new_genre_mean)]
            
            for i in range(len(similar_indices[0])):
                title = movies_info_final['Title'][similar_indices[0][i]]
                if((title in movies) or (title in movies_already_choosen)):
                    continue
                X.append(list(movies_info_final.loc[similar_indices[0][i], genres]))
                y.append(title)
                movies_already_choosen.append(title)
     
    genre_mean = [x/3 for x in genre_mean]
    return X, y, genre_mean    
    
    
def find(movies):
    X, y, genre_mean = similar_movie(movies, movies_info_final, cosine_similarities_total)
    neigh = KNeighborsRegressor(n_neighbors=10)
    neigh.fit(X, y)
    movies_index = neigh.kneighbors(np.reshape(genre_mean, (1, -1)))[1][0]
    ret = [y[i] for i in movies_index]
    return ret
    
def get_movies():
    return np.array(movies_info_final["Title"])
