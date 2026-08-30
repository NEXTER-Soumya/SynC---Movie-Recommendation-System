import streamlit as st

from recommender import (
    recommend,
    movies,
    get_movie_details
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SynC - Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# TMDB API KEY
# ============================================================

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


# ============================================================
# SESSION STATE
# ============================================================

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

    /* ========================================================
       APP
       ======================================================== */

    .stApp {
        background-color: #141414;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 4%;
        padding-right: 4%;
        padding-bottom: 4rem;
    }


    /* ========================================================
       HIDE STREAMLIT DEFAULT UI
       ======================================================== */

    header[data-testid="stHeader"] {
        display: none;
    }

    #MainMenu {
        display: none;
    }

    footer {
        display: none;
    }

    [data-testid="stToolbar"] {
        display: none;
    }


    /* ========================================================
       LOGO
       ======================================================== */

    .logo {
        color: #E50914;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 4rem;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero-title {
        color: white;
        font-size: 3.2rem;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 0.8rem;
    }

    .hero-subtitle {
        color: #b3b3b3;
        font-size: 1.15rem;
        margin-bottom: 2.5rem;
    }


    /* ========================================================
       SELECT BOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        background-color: #242424;
        border: 1px solid #3a3a3a;
        border-radius: 5px;
        min-height: 48px;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    div.stButton > button {
        width: 100%;
        min-height: 45px;

        background-color: #E50914;
        color: white;

        border: none;
        border-radius: 5px;

        font-size: 0.95rem;
        font-weight: 600;

        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #b20710;
        color: white;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        color: white;
        font-size: 1.6rem;
        font-weight: 600;

        margin-top: 3rem;
        margin-bottom: 1.5rem;
    }


    /* ========================================================
       MOVIE TITLE
       ======================================================== */

    .movie-title {
        color: white;
        font-size: 1rem;
        font-weight: 600;

        margin-top: 0.7rem;
        margin-bottom: 0.8rem;

        min-height: 45px;
    }


    /* ========================================================
       DETAIL PAGE
       ======================================================== */

    .detail-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;

        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .detail-rating {
        color: #f5c518;
        font-size: 1.1rem;
        font-weight: 600;

        margin-bottom: 1rem;
    }

    .detail-meta {
        color: #b3b3b3;
        font-size: 1rem;

        margin-bottom: 1.5rem;
    }

    .detail-heading {
        color: white;
        font-size: 1.3rem;
        font-weight: 600;

        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }

    .detail-text {
        color: #d0d0d0;
        line-height: 1.7;
        font-size: 1rem;
    }

    .actor-name {
        color: white;
        font-size: 0.9rem;
        font-weight: 600;

        text-align: center;

        margin-top: 0.5rem;
    }

    .director-name {
        color: white;
        font-size: 1rem;
        font-weight: 600;

        margin-top: 0.5rem;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #666666;
        font-size: 0.85rem;

        margin-top: 5rem;
        padding-top: 2rem;

        border-top: 1px solid #292929;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_image_url(path, size="w500"):
    """
    Convert a TMDB image path into a complete image URL.
    """

    if not path:
        return None

    return f"https://image.tmdb.org/t/p/{size}{path}"


def get_profile_url(profile_path):
    """
    Convert actor/director profile path into image URL.
    """

    if not profile_path:
        return None

    return f"https://image.tmdb.org/t/p/w185{profile_path}"


@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    """
    Fetch movie details from TMDB.
    """

    return get_movie_details(
        movie_id,
        TMDB_API_KEY
    )


def get_movie_row(title):
    """
    Get a movie row from our dataframe.
    """

    result = movies[
        movies["title"] == title
    ]

    if result.empty:
        return None

    return result.iloc[0]


# ============================================================
# MOVIE DETAIL PAGE
# ============================================================

if st.session_state.selected_movie:

    selected = st.session_state.selected_movie

    movie_row = get_movie_row(selected)

    if movie_row is None:

        st.error("Movie not found.")

        if st.button("← Back"):

            st.session_state.selected_movie = None
            st.rerun()

    else:

        movie_id = movie_row["id"]

        # ----------------------------------------------------
        # FETCH DETAILS
        # ----------------------------------------------------

        try:

            details = fetch_movie_details(
                movie_id
            )

        except Exception as e:

            st.error(
                f"TMDB request failed: {e}"
            )

            st.stop()


        # ----------------------------------------------------
        # BACK BUTTON
        # ----------------------------------------------------

        if st.button("← Back to recommendations"):

            st.session_state.selected_movie = None
            st.rerun()


        # ----------------------------------------------------
        # BACKDROP
        # ----------------------------------------------------

        backdrop_url = get_image_url(
            details.get("backdrop_path"),
            "original"
        )

        if backdrop_url:

            st.image(
                backdrop_url,
                use_container_width=True
            )


        # ----------------------------------------------------
        # POSTER + MAIN INFORMATION
        # ----------------------------------------------------

        poster_col, info_col = st.columns(
            [1, 2.5],
            gap="large"
        )


        with poster_col:

            poster_url = get_image_url(
                details.get("poster_path"),
                "w500"
            )

            if poster_url:

                st.image(
                    poster_url,
                    use_container_width=True
                )

            else:

                st.write("Poster unavailable")


        with info_col:

            # ------------------------------------------------
            # TITLE
            # ------------------------------------------------

            st.markdown(
                f'<div class="detail-title">'
                f'{details.get("title", selected)}'
                f'</div>',
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # RATING
            # ------------------------------------------------

            rating = details.get(
                "vote_average",
                0
            )

            st.markdown(
                f'<div class="detail-rating">'
                f'⭐ {rating:.1f}/10'
                f'</div>',
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # RUNTIME
            # ------------------------------------------------

            runtime = details.get("runtime")

            if runtime:

                runtime_text = f"{runtime} min"

            else:

                runtime_text = "N/A"


            st.markdown(
                f'<div class="detail-meta">'
                f'⏱ {runtime_text}'
                f'</div>',
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # OVERVIEW
            # ------------------------------------------------

            st.markdown(
                '<div class="detail-heading">'
                'Overview'
                '</div>',
                unsafe_allow_html=True
            )

            overview = details.get(
                "overview",
                "No overview available."
            )

            st.markdown(
                f'<div class="detail-text">'
                f'{overview}'
                f'</div>',
                unsafe_allow_html=True
            )


        # ====================================================
        # DIRECTOR
        # ====================================================

        st.markdown(
            '<div class="detail-heading">'
            'Director'
            '</div>',
            unsafe_allow_html=True
        )


        crew = details.get(
            "credits",
            {}
        ).get(
            "crew",
            []
        )


        director = None

        for person in crew:

            if person.get("job") == "Director":

                director = person
                break


        if director:

            director_col1, director_col2 = st.columns(
                [0.5, 4],
                gap="medium"
            )


            with director_col1:

                director_image = get_profile_url(
                    director.get("profile_path")
                )

                if director_image:

                    st.image(
                        director_image,
                        use_container_width=True
                    )

                else:

                    st.write("No image")


            with director_col2:

                st.markdown(
                    f'<div class="director-name">'
                    f'{director.get("name", "Unknown")}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        else:

            st.write("Director information unavailable.")


        # ====================================================
        # TOP 5 CAST
        # ====================================================

        st.markdown(
            '<div class="detail-heading">'
            'Top 5 Cast'
            '</div>',
            unsafe_allow_html=True
        )


        cast = details.get(
            "credits",
            {}
        ).get(
            "cast",
            []
        )


        top_cast = cast[:5]


        if top_cast:

            cast_columns = st.columns(
                len(top_cast),
                gap="medium"
            )


            for col, actor in zip(
                cast_columns,
                top_cast
            ):

                with col:

                    actor_name = actor.get(
                        "name",
                        "Unknown"
                    )

                    actor_image = get_profile_url(
                        actor.get("profile_path")
                    )


                    if actor_image:

                        st.image(
                            actor_image,
                            use_container_width=True
                        )

                    else:

                        st.write(
                            "No image available"
                        )


                    st.markdown(
                        f'<div class="actor-name">'
                        f'{actor_name}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

        else:

            st.write(
                "Cast information unavailable."
            )


# ============================================================
# HOME PAGE
# ============================================================

else:

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="logo">SynC - Movie Recommendation System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">'
        'Find your next movie.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Choose a movie and discover titles you might enjoy.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # MOVIE SELECTOR
    # --------------------------------------------------------

    select_col, button_col = st.columns(
        [5, 1],
        gap="medium"
    )


    with select_col:

        selected_movie = st.selectbox(
            "Select a movie",
            movies["title"].values,
            label_visibility="collapsed"
        )


    with button_col:

        recommend_clicked = st.button(
            "Recommend"
        )


    # --------------------------------------------------------
    # GENERATE RECOMMENDATIONS
    # --------------------------------------------------------

    if recommend_clicked:

        recommendations = recommend(
            selected_movie
        )

        st.session_state.recommendations = recommendations

        st.rerun()


    # --------------------------------------------------------
    # SHOW RECOMMENDATIONS
    # --------------------------------------------------------

    if st.session_state.recommendations:

        recommendations = st.session_state.recommendations


        st.markdown(
            '<div class="section-title">'
            'Top picks for you'
            '</div>',
            unsafe_allow_html=True
        )


        # ====================================================
        # ROW 1
        # ====================================================

        columns = st.columns(
            5,
            gap="medium"
        )


        for i, col in enumerate(columns):

            movie_title = recommendations[i]

            movie_row = get_movie_row(
                movie_title
            )


            with col:

                movie_id = movie_row["id"]


                # --------------------------------------------
                # FETCH POSTER
                # --------------------------------------------

                try:

                    details = fetch_movie_details(
                        movie_id
                    )

                    poster_url = get_image_url(
                        details.get("poster_path"),
                        "w500"
                    )

                except Exception as e:

                    poster_url = None


                # --------------------------------------------
                # POSTER
                # --------------------------------------------

                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.markdown(
                        "Poster unavailable"
                    )


                # --------------------------------------------
                # TITLE
                # --------------------------------------------

                st.markdown(
                    f'<div class="movie-title">'
                    f'{movie_title}'
                    f'</div>',
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # VIEW BUTTON
                # --------------------------------------------

                if st.button(
                    "View Details",
                    key=f"movie_{i}"
                ):

                    st.session_state.selected_movie = movie_title

                    st.rerun()


        # ====================================================
        # ROW 2
        # ====================================================

        columns = st.columns(
            5,
            gap="medium"
        )


        for i, col in enumerate(
            columns,
            start=5
        ):

            movie_title = recommendations[i]

            movie_row = get_movie_row(
                movie_title
            )


            with col:

                movie_id = movie_row["id"]


                # --------------------------------------------
                # FETCH POSTER
                # --------------------------------------------

                try:

                    details = fetch_movie_details(
                        movie_id
                    )

                    poster_url = get_image_url(
                        details.get("poster_path"),
                        "w500"
                    )

                except Exception as e:

                    poster_url = None


                # --------------------------------------------
                # POSTER
                # --------------------------------------------

                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.markdown(
                        "Poster unavailable"
                    )


                # --------------------------------------------
                # TITLE
                # --------------------------------------------

                st.markdown(
                    f'<div class="movie-title">'
                    f'{movie_title}'
                    f'</div>',
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # VIEW BUTTON
                # --------------------------------------------

                if st.button(
                    "View Details",
                    key=f"movie_{i}"
                ):

                    st.session_state.selected_movie = movie_title

                    st.rerun()


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown(
        '<div class="footer">'
        'SynC • Content-Based Movie Recommendation System'
        '</div>',
        unsafe_allow_html=True
    )