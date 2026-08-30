<img width="1905" height="1080" alt="image" src="https://github.com/user-attachments/assets/840a02df-6a51-4eab-a417-75c642947547" />

# 🎬 CineMatch — Movie Recommendation System

CineMatch is a content-based movie recommendation system built with Python, scikit-learn, NLTK, Streamlit, and the TMDB API.

The system recommends movies based on the similarity of their textual and metadata features rather than relying on user ratings or collaborative filtering.

The project was developed in two stages:
1. Build and test the recommendation engine in `mrc.ipynb`.
2. Convert the model into a Streamlit web application with movie posters, backdrops, cast, director, rating, runtime, and overview.

---

## 📌 What Is This Project?

CineMatch answers:

> **“I like this movie. What other movies should I watch?”**

A user selects a movie, the recommendation engine compares it with the other movies in the dataset, and the system returns the **top 10 most similar movies**.

The recommendation information is built from:

- Movie overview
- Genres
- Keywords
- Cast
- Director
- Production companies

These fields are combined into a single textual feature called `tags`.

### Overall Pipeline

```text
Movie Metadata
      ↓
Data Cleaning
      ↓
Feature Engineering
      ↓
Text Normalization
      ↓
Stemming
      ↓
CountVectorizer
      ↓
Movie Vectors
      ↓
Cosine Similarity
      ↓
Ranking
      ↓
Top 10 Recommendations
      ↓
Streamlit UI + TMDB API
```

---

# ✨ Features

## Recommendation Engine

- Content-based movie recommendation
- Top 10 recommendations
- Porter stemming
- English stop-word removal
- CountVectorizer
- Maximum 5,000 text features
- Cosine similarity
- Similarity used internally for ranking, but not shown to users

## Web Application

- Netflix-inspired dark UI
- Movie selection dropdown
- Recommendation button
- 10 movie recommendations in a poster grid
- Movie detail view
- Backdrop image
- Original poster
- Movie title
- Rating
- Runtime
- Overview
- Director
- Director image
- Top 5 cast members
- Cast profile images
- Back navigation

## TMDB Integration

TMDB is used to provide movie imagery and additional movie/credit information for the web interface.

---

# 🧠 Recommendation Engine

## 1. Dataset

The project uses the following files:

```text
tmdb_5000_movies.csv
tmdb_5000_credits.csv
```

The movie and credits datasets are merged using the movie title.

The resulting dataframe contains both movie metadata and cast/crew information.

---

## 2. Data Cleaning

Columns that are not required by the current recommendation/UI workflow are removed, while important fields such as the movie ID, title, overview, runtime, rating, genres, keywords, cast, and crew are retained.

The movie ID is particularly important because it is used to connect a dataset movie to TMDB API information.

---

# 🏗️ Feature Engineering

The main feature used by the recommendation engine is `tags`.

The following information is combined:

```text
overview
genres
cast
crew
keywords
production_companies
```

Conceptually:

```text
Overview
   +
Genres
   +
Keywords
   +
Cast
   +
Director
   +
Production Companies
        ↓
      tags
```

For example, a movie can be represented by text containing concepts similar to:

```text
space alien planet astronaut sciencefiction action adventure
```

The purpose is to create one text representation of a movie that can be compared against other movie representations.

---

# 🔤 Text Preprocessing

Before vectorization, the tags are normalized.

## Lowercasing

Text is converted to lowercase so that variations such as:

```text
Action
action
ACTION
```

are treated consistently.

## Tokenization

The movie overview is split into individual words.

## Metadata normalization

Multi-word metadata values are normalized so that they remain meaningful as metadata features.

## Stemming

The project uses NLTK's `PorterStemmer`.

For example:

```text
dance
dancing
danced
dances
```

can be reduced to a common stem such as:

```text
danc
```

The purpose is to reduce different morphological forms into a smaller set of features.

---

# 🔢 Vectorization

After preprocessing, the `tags` field is converted into numerical vectors using:

```python
CountVectorizer(
    max_features=5000,
    stop_words="english"
)
```

CountVectorizer creates a document-term matrix.

Conceptually:

```text
                 alien  action  space  romance  crime
Movie A             2       1      4        0      0
Movie B             3       1      3        0      0
Movie C             0       0      0        4      2
```

Each row represents one movie.

Each column represents one vocabulary feature.

The resulting matrix is stored in:

```python
vectors
```

---

# 📐 Cosine Similarity

The movie vectors are compared using cosine similarity.

The formula is:

\[
	ext{Similarity}(A,B)
=
rac{A \cdot B}
{||A||\,||B||}
\]

The similarity matrix is stored in:

```python
similarity
```

Each row contains the similarity of one movie against all movies.

This transforms recommendation into a ranking problem:

```text
Selected movie
      ↓
Compare with every movie
      ↓
Calculate similarity
      ↓
Sort highest → lowest
      ↓
Return top 10
```

---

# 🎯 Recommendation Function

The `recommend()` function performs the following steps:

1. Find the selected movie in the dataframe.
2. Obtain its similarity scores.
3. Pair movie indices with similarity scores.
4. Sort them by descending similarity.
5. Skip the selected movie itself.
6. Return the next 10 movie titles.

The ranking uses:

```python
movies_list = sorted(
    list(enumerate(distances)),
    key=lambda x: x[1],
    reverse=True
)[1:11]
```

`[1:11]` is used because index `0` is the selected movie itself.

The final function returns only movie titles, for example:

```python
[
    "Movie A",
    "Movie B",
    "Movie C",
    "Movie D",
    "Movie E"
]
```

Similarity values are used internally and are not displayed in the application.

---

# 🌐 Streamlit Application

The machine-learning model is exposed through a Streamlit web application.

The application has two main states:

```text
HOME PAGE
    ↓
Select Movie
    ↓
Recommend
    ↓
Top 10 Movie Posters
    ↓
View Details
    ↓
MOVIE DETAIL PAGE
```

The recommendation engine remains in `recommender.py`, while the UI is handled by `app.py`.

This keeps the project separated into:

```text
Machine Learning / Backend
        +
Web Application / Frontend
```

---

# 🎨 User Interface

The UI uses a dark cinematic design inspired by streaming platforms.

The main page contains:

```text
CINEMATCH

Find your next movie.

Choose a movie and discover titles you might enjoy.

[ Select a movie                         ] [ Recommend ]

Top picks for you

[ Poster ][ Poster ][ Poster ][ Poster ][ Poster ]

[ Poster ][ Poster ][ Poster ][ Poster ][ Poster ]
```

The design uses:

- Near-black background
- White text
- Dark gray surfaces
- Red accent buttons
- Minimal borders
- Poster-focused recommendations

The project is inspired by streaming-platform design patterns but is not affiliated with Netflix.

---

# 🎞️ Movie Detail Page

Clicking **View Details** opens a movie detail view.

The page contains:

```text
Backdrop Image

Poster        Movie Title
              ⭐ Rating
              ⏱ Runtime

              Overview
              ...

Director

[Director Image]  Director Name

Top 5 Cast

[Actor] [Actor] [Actor] [Actor] [Actor]
 Name    Name    Name    Name    Name
```

The application obtains cast and crew information and displays profile images where TMDB provides them.

---

# 🔌 TMDB API Integration

The application uses the movie's TMDB ID from the dataset to retrieve additional details and images.

The API integration is used for information such as:

- Poster path
- Backdrop path
- Rating
- Runtime
- Overview
- Cast information
- Director information
- Profile images

TMDB image paths are converted into usable image URLs inside the application.

---

# 🔐 API Key Security

The TMDB API key is not stored directly in `app.py` or `recommender.py`.

It is stored locally in:

```text
.streamlit/secrets.toml
```

Example:

```toml
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
```

The application reads it using:

```python
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
```

The real `secrets.toml` must never be pushed to GitHub.

The `.gitignore` file includes:

```gitignore
.streamlit/secrets.toml
venv/
.venv/
__pycache__/
*.pyc
```

---

# 📁 Project Structure

```text
Movie Recommendation System/
│
├── app.py
├── recommender.py
├── mrc.ipynb
│
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
│
├── requirements.txt
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

## `app.py`

The Streamlit frontend.

Responsibilities:

- Page configuration
- Styling
- Movie selection
- Recommendation display
- Poster display
- Movie detail page
- Backdrop display
- Cast/director display
- Session-state navigation
- TMDB image integration

## `recommender.py`

The recommendation backend.

Responsibilities:

- Load datasets
- Merge datasets
- Clean data
- Extract cast/director
- Construct `tags`
- Stem text
- Vectorize text
- Calculate cosine similarity
- Generate top 10 recommendations
- Provide TMDB request helper

## `mrc.ipynb`

The original development and experimentation notebook.

It was used to build, test, and understand the recommendation pipeline before separating the model into `recommender.py`.

## `tmdb_5000_movies.csv`

Movie-level metadata.

## `tmdb_5000_credits.csv`

Cast and crew information.

## `.streamlit/secrets.toml`

Local secret configuration containing the TMDB API key.

This file must remain private.

---

# ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data processing |
| Scikit-learn | Vectorization and similarity |
| NLTK | Stemming |
| CountVectorizer | Text-to-vector conversion |
| Cosine Similarity | Movie similarity calculation |
| Streamlit | Web application |
| Requests | HTTP/API requests |
| TMDB API | Movie details and images |
| Jupyter Notebook | Model development |
| Git/GitHub | Version control and hosting |

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "Movie Recommendation System"
```

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scriptsctivate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
streamlit
pandas
scikit-learn
nltk
requests
```

---

# 🔑 Configure TMDB

Create:

```text
.streamlit/
```

and inside it:

```text
secrets.toml
```

Add:

```toml
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
```

Do not commit the real file to GitHub.

---

# ▶️ Run the Application

Activate the virtual environment and run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL.

Open that URL in your browser to use CineMatch.

---

# 🧪 How to Use CineMatch

1. Open the application.
2. Select a movie.
3. Click **Recommend**.
4. The recommendation engine calculates similarity against the movie dataset.
5. The top 10 recommendations are displayed.
6. Movie posters are loaded through TMDB.
7. Click **View Details** on a recommended movie.
8. Explore its poster, backdrop, rating, runtime, overview, director, and top five cast members.

---

# 🧩 System Architecture

```text
                    USER
                     │
                     ▼
             ┌─────────────────┐
             │   Streamlit UI  │
             │      app.py     │
             └────────┬────────┘
                      │
                Select Movie
                      │
                      ▼
             ┌─────────────────┐
             │ Recommendation  │
             │     Engine      │
             │ recommender.py   │
             └────────┬────────┘
                      │
                      ▼
                Movie Metadata
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   Feature Engineering       Data Processing
          │                       │
          └───────────┬───────────┘
                      ▼
                     Tags
                      │
                      ▼
                 Stemming
                      │
                      ▼
              CountVectorizer
                      │
                      ▼
                Movie Vectors
                      │
                      ▼
              Cosine Similarity
                      │
                      ▼
                 Top 10 Movies
                      │
                      ▼
             ┌─────────────────┐
             │     TMDB API    │
             └────────┬────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     Posters      Backdrops      Movie Info
                                      │
                                      ▼
                            Movie Detail Page
```

---

# 🧠 Why Content-Based?

CineMatch is content-based because recommendations are determined from **movie characteristics**.

The system does not require:

```text
User A → Movie X → 5 stars
User B → Movie X → 4 stars
```

Instead, it compares the content representation of one movie against another:

```text
Movie A
  ↓
Feature Vector A

Movie B
  ↓
Feature Vector B

Vector A ↔ Vector B
       ↓
Similarity
       ↓
Recommendation
```

This means a user can receive recommendations without providing a history of previous interactions.

---

# 📊 Current Model Characteristics

The current model is intentionally simple and interpretable.

## Strengths

- Simple architecture
- Easy to understand
- Easy to debug
- No user history required
- No user accounts required
- Works immediately for new users
- Fast enough for the current dataset
- Uses interpretable textual features

## Limitations

Because the current model uses CountVectorizer, recommendations depend strongly on the chosen vocabulary and metadata.

The model primarily identifies overlap between textual features rather than deep semantic relationships.

For example:

```text
car
```

and:

```text
automobile
```

may be represented as different features.

The system also does not currently use:

- User preferences
- Watch history
- Personal ratings
- Collaborative filtering
- Deep semantic embeddings
- Personalized ranking
- Time-dependent preferences

---

# 🔬 Future Improvements

## TF-IDF

Replace CountVectorizer with TF-IDF so that common words have less influence and more informative terms receive greater weight.

```text
Current:
CountVectorizer

Possible improvement:
TfidfVectorizer
```

## Semantic Embeddings

Use models such as:

```text
Word2Vec
GloVe
BERT
Sentence Transformers
```

to represent semantic meaning in dense vector spaces.

Possible pipeline:

```text
Movie Text
     ↓
Embedding Model
     ↓
Dense Vector
     ↓
Similarity
     ↓
Recommendation
```

## Hybrid Recommendation

Combine content-based information with user behavior:

```text
Content Similarity
       +
User Ratings
       +
Watch History
       +
Popularity
       ↓
Hybrid Recommendation
```

## Better Evaluation

A production-quality version should evaluate recommendation quality using ranking metrics such as:

```text
Precision@K
Recall@K
MAP@K
NDCG@K
```

A conventional classification accuracy score is not directly appropriate unless a reliable ground-truth relevance definition is available.

## Production Improvements

Possible future improvements include:

- Better recommendation ranking
- Faster similarity search
- More scalable storage
- Database integration
- Search instead of a large dropdown
- Personalized accounts
- Responsive mobile UI
- Deployment
- Automated testing
- Logging and monitoring

---

# 📜 Data and Attribution

The recommendation model uses the TMDB 5000 movie and credits datasets.

Movie posters, backdrops, and additional movie information are retrieved through TMDB services.

This is an educational/student project and is not affiliated with Netflix.

When publicly deploying the application, follow the current TMDB attribution and API usage requirements.

---

# 🔒 Security

Never commit:

```text
.streamlit/secrets.toml
```

to GitHub.

Before pushing the project, run:

```bash
git status
```

and verify that your API secret is not staged.

If a real API key is ever accidentally exposed publicly, revoke or rotate it.

---

# ✅ Current Project Status

### Completed

- [x] Dataset loading
- [x] Dataset merging
- [x] Data cleaning
- [x] Feature engineering
- [x] Tag creation
- [x] Text normalization
- [x] Porter stemming
- [x] CountVectorizer
- [x] Cosine similarity
- [x] Top 10 recommendations
- [x] Streamlit application
- [x] Netflix-inspired dark UI
- [x] Movie posters
- [x] Movie backdrop
- [x] Movie detail page
- [x] Movie rating
- [x] Movie runtime
- [x] Movie overview
- [x] Director information
- [x] Director image
- [x] Top 5 cast
- [x] Cast profile images
- [x] API key stored using Streamlit secrets
- [x] GitHub-safe `.gitignore`

### Future Work

- [ ] TF-IDF comparison
- [ ] Semantic embeddings
- [ ] Hybrid recommendation
- [ ] Recommendation evaluation
- [ ] Search interface
- [ ] User personalization
- [ ] Database integration
- [ ] Improved scalability
- [ ] Production deployment

---

# 👨‍💻 Project Summary

CineMatch demonstrates an end-to-end machine-learning application:

```text
Data
 ↓
Preprocessing
 ↓
Feature Engineering
 ↓
NLP
 ↓
Vectorization
 ↓
Similarity
 ↓
Recommendation
 ↓
Web Application
 ↓
API Integration
```

The project combines:

```text
Machine Learning
+
Natural Language Processing
+
Data Processing
+
Web Development
+
REST API Integration
```

into a complete interactive movie recommendation system.

---

## ⭐ Core Idea

At the heart of CineMatch is a simple mathematical idea:

\[
oxed{
	ext{Movie Content}

ightarrow
	ext{Numerical Representation}

ightarrow
	ext{Similarity}

ightarrow
	ext{Ranking}

ightarrow
	ext{Recommendation}
}
\]

The result is a movie recommendation application that takes a movie a user already likes and finds other movies with similar content.
