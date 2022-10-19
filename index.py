# https://techvidvan.com/tutorials/movie-recommendation-system-python-machine-learning/
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from ast import literal_eval

# read file
path = "./data"
credits_df = pd.read_csv("./dataset/tmdb_5000_credits.csv")
movies_df = pd.read_csv("./dataset/tmdb_5000_movies.csv")

# merge
credits_df.columns = ['id', 'title', 'cast', 'crew']
movies_df = movies_df.merge(credits_df, on="id")

# convert the data into a safe and usable structure.
features = ["cast", "crew", "keywords", "genres"]
for feature in features:
    movies_df[feature] = movies_df[feature].apply(literal_eval)


def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan

# get the top 3 elements or the entire list whichever is more.


def get_list(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []


movies_df["director"] = movies_df["crew"].apply(get_director)
features = ["cast", "keywords", "genres"]
for feature in features:
    movies_df[feature] = movies_df[feature].apply(get_list)

# convert the above feature instances into lowercase and remove all the spaces between them


def clean_data(row):
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""


features = ['cast', 'keywords', 'director', 'genres']
for feature in features:
    movies_df[feature] = movies_df[feature].apply(clean_data)


# create a “soup” containing all of the metadata information extracted to input into the vectorizer.
def create_soup(features):
    return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features['director'] + ' ' + ' '.join(features['genres'])


movies_df["soup"] = movies_df.apply(create_soup, axis=1)

count_vectorizer = CountVectorizer(stop_words="english")
count_matrix = count_vectorizer.fit_transform(movies_df["soup"])

print(count_matrix)
cosine_sim = cosine_similarity(count_matrix, count_matrix)

movies_df = movies_df.reset_index()
indices = pd.Series(movies_df.index, index=movies_df["id"]).drop_duplicates()


def get_recommendations(id, cosine_sim=cosine_sim):
    idx = indices[id]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(
        similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:11]
    # (a, b) where a is id of movie, b is similarity_scores

    movies_indices = [ind[0] for ind in similarity_scores]
    movies = movies_df["id"].iloc[movies_indices]
    return movies


# print("################ Content Based System #############")
# print("Recommendations for Avatar")
# print(get_recommendations(19995))
# print()
# print("Recommendations for Avengers")
# print(get_recommendations("The Avengers", cosine_sim))
