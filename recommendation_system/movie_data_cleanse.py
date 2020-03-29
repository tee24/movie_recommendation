import pandas as pd
import re
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def fetch_keywords(keywords):
	tags = ""
	try:
		keywords = eval(keywords[1:-1])
	except:
		return ""

	for i in keywords:
		try:
			if i == 0:
				tags = tags + f"{i['name']}"
			else:
				tags = tags + f" {i['name']}"
		except:
			pass
	tags.lower()
	return tags


def fetch_director(crew):
	try:
		crew = eval(crew[1:-1])
		for x in crew:
			if x['job'] == 'Director':
				return x['name'].lower().replace(" ", "")
		return ""
	except:
		return ""

def fetch_cast(cast, number=2):
	cast_names = []
	try:
		cast = eval(cast[1:-1])
	except:
		return ""

	for i in range(number):
		try:
			cast_names.append(cast[i]['name'])
		except:
			pass
	return ' '.join([x.lower().replace(" ", "") for x in cast_names])

def fetch_genre(genre):
	genres = ""
	try:
		genre = eval(genre[1:-1])
	except:
		return ""

	for i in genre:
		try:
			if i == 0:
				genres = genres + i['name'].lower()
			else:
				genres = genres + " " + i['name'].lower()

		except:
			pass
	return genres

def trim(string):
	return ' '.join(string.split())

def clean(string):
	return re.sub('[^A-Za-z0-9 ]+', '', string)

movies = pd.read_csv('data\movies_metadata.csv', low_memory=False, dtype={'id': int})
credits = pd.read_csv('data\credits.csv', dtype={'id': int})
keywords = pd.read_csv('data\keywords.csv', dtype={'id': int})

movies = movies.merge(credits, on='id')
movies = movies.merge(keywords, on='id')

movies['director'] = movies['crew'].apply(fetch_director)
movies['actors'] = movies['cast'].apply(fetch_cast)
movies['tags'] = movies['keywords'].apply(fetch_keywords)
movies['genres'] = movies['genres'].apply(fetch_genre)
movies['features'] = movies['director'] + " " + movies['actors'] + " " + movies['tags'] + " " + movies['genres']
movies['features'] = movies['features'].apply(trim)
movies['features'] = movies['features'].apply(clean)

movies_trim = movies[['id', 'imdb_id', 'title', 'vote_average', 'vote_count', 'features']]
movies_trim.to_csv('movies.csv')