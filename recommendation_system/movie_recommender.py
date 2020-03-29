import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('movie.csv')

def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]


def recommendations(title):
	vec = CountVectorizer()
	count_mat = vec.fit_transform(df['features'])
	cosine_sim = cosine_similarity(count_mat)
	movie_index = get_index_from_title(title)

	similar_movies = list(enumerate(cosine_sim[movie_index]))

	sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

	for i in range(10):
		print(get_title_from_index(sorted_similar_movies[i][0]))
