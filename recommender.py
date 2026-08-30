import ast
import requests
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer


# ============================================================
# LOAD DATA
# ============================================================

movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")


# ============================================================
# MERGE DATA
# ============================================================

movies = movies.merge(credits, on="title")


# ============================================================
# DROP UNNECESSARY COLUMNS
# ============================================================

movies = movies.drop(
    [
        "budget",
        "homepage",
        "original_language",
        "original_title",
        "popularity",
        "production_countries",
        "release_date",
        "revenue",
        "spoken_languages",
        "status",
        "vote_count",
        "tagline",
    ],
    axis=1,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def convert(obj):
    result = []

    for item in ast.literal_eval(obj):
        result.append(item["name"])

    return result


def get_top_actors(obj):
    result = []

    for item in ast.literal_eval(obj)[:5]:
        result.append(item["name"])

    return result


def get_director(obj):
    for item in ast.literal_eval(obj):
        if item["job"] == "Director":
            return item["name"]

    return "Unknown"


# ============================================================
# HANDLE MISSING VALUES
# ============================================================

movies["overview"] = movies["overview"].fillna("")

movies["genres"] = movies["genres"].fillna("[]")
movies["keywords"] = movies["keywords"].fillna("[]")
movies["production_companies"] = movies["production_companies"].fillna("[]")
movies["cast"] = movies["cast"].fillna("[]")
movies["crew"] = movies["crew"].fillna("[]")


# ============================================================
# EXTRACT ACTORS + DIRECTOR FOR UI
# ============================================================

movies["actors"] = movies["cast"].apply(get_top_actors)

movies["director"] = movies["crew"].apply(get_director)


# ============================================================
# CONVERT JSON-LIKE COLUMNS
# ============================================================

movies["genres"] = movies["genres"].apply(convert)

movies["keywords"] = movies["keywords"].apply(convert)

movies["production_companies"] = movies[
    "production_companies"
].apply(convert)


# ============================================================
# PREPARE OVERVIEW
# ============================================================

movies["overview"] = movies["overview"].apply(
    lambda x: x.split()
)


# ============================================================
# REMOVE SPACES FROM NAMES
# ============================================================

movies["cast"] = movies["cast"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["crew"] = movies["crew"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["genres"] = movies["genres"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["keywords"] = movies["keywords"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["production_companies"] = movies[
    "production_companies"
].apply(
    lambda x: [i.replace(" ", "") for i in x]
)


# ============================================================
# CREATE TAGS
# ============================================================

movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["cast"]
    + movies["crew"]
    + movies["keywords"]
    + movies["production_companies"]
)


# ============================================================
# TAGS -> STRING
# ============================================================

movies["tags"] = movies["tags"].apply(
    lambda x: " ".join(x)
)

movies["tags"] = movies["tags"].str.lower()


# ============================================================
# STEMMING
# ============================================================

ps = PorterStemmer()


def stemming(text):
    result = []

    for word in text.split():
        result.append(ps.stem(word))

    return " ".join(result)


movies["tags"] = movies["tags"].apply(stemming)


# ============================================================
# COUNT VECTORIZATION
# ============================================================

cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

vectors = cv.fit_transform(
    movies["tags"]
).toarray()


# ============================================================
# COSINE SIMILARITY
# ============================================================

similarity = cosine_similarity(vectors)


# ============================================================
# RECOMMEND 10 MOVIES
# ============================================================

def recommend(movie):

    matching_movies = movies[
        movies["title"] == movie
    ]

    if matching_movies.empty:
        return []

    index = matching_movies.index[0]

    distances = similarity[index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:11]

    return [
        movies.iloc[idx]["title"]
        for idx, score in movies_list
    ]


# ============================================================
# TMDB API
# ============================================================

def get_movie_details(movie_id, api_key):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "accept": "application/json"
    }

    params = {
        "api_key": api_key,
        "append_to_response": "credits"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()