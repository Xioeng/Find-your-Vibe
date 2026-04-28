import os
import sys

import streamlit as st

ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from find_your_vibe.domain.song import Song
from find_your_vibe.domain.user_preferences import UserProfile
from find_your_vibe.recommender.recommender import Recommender
from find_your_vibe.services.artist_discovery_service import ArtistDiscoveryService

# Ensure src is on path so imports work when running from repo root


GEMINI_MODELS = [
    "gemini-3.1-flash-lite-preview",
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

MOOD_OPTIONS = [
    "😊 Happy",
    "😔 Sad",
    "😴 Calm",
    "⚡ Energetic",
    "😤 Angry",
    "😌 Peaceful",
    "😍 Romantic",
    "😂 Playful",
    "😰 Anxious",
    "😐 Neutral",
]


# Initialize session state
if "liked_songs" not in st.session_state:
    st.session_state.liked_songs = []
if "new_song_title" not in st.session_state:
    st.session_state.new_song_title = ""
if "new_song_artist" not in st.session_state:
    st.session_state.new_song_artist = ""


def _validate_api_key():
    """Validate Gemini API key, return (key, model) or (None, None)."""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        api_key = st.text_input("🔑 Gemini API key", type="password")
        gemini_model = st.selectbox(
            "🤖 Select Gemini model", options=GEMINI_MODELS, index=0
        )

        if api_key:
            st.success("✅ Gemini key configured")
            st.info(f"📦 Model: {gemini_model}")
        else:
            st.warning("⚠️ Please provide your Gemini API key to proceed")
            return None, None

    return api_key, gemini_model


def _display_header():
    """Display app header and subtitle."""
    st.markdown(
        '<div class="main-header">🎵 Find Your Vibe</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Discover music tailored to your taste</div>',
        unsafe_allow_html=True,
    )


def _get_user_profile():
    """Collect user profile inputs, return profile dict."""
    st.markdown("## 👤 Create Your Profile", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(
            "👤 Your name", value="Guest", placeholder="Enter your name"
        )
    with col2:
        favorite_genre = st.text_input(
            "🎸 Favorite genre", value="pop", placeholder="e.g., pop, rock, jazz"
        )

    col1, col2 = st.columns(2)
    with col1:
        favorite_mood = st.selectbox(
            "😊 Favorite mood",
            options=MOOD_OPTIONS,
            index=0,
            help="Choose the mood you most enjoy in music",
        )
    with col2:
        target_energy = st.slider(
            "⚡ Target energy level",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.01,
        )

    likes_acoustic = st.checkbox("🎸 I like acoustic music", value=False)

    return {
        "name": name,
        "favorite_genre": favorite_genre,
        "favorite_mood": favorite_mood,
        "target_energy": target_energy,
        "likes_acoustic": likes_acoustic,
    }


def _display_liked_songs():
    """Display and manage liked songs section."""
    st.markdown("## ❤️ Songs You Like (Optional)", unsafe_allow_html=True)
    st.markdown("Add your favorite songs to personalize recommendations")

    if st.session_state.liked_songs:
        st.markdown("### Your Liked Songs:")
        for idx, song_info in enumerate(st.session_state.liked_songs):
            col_song, col_delete = st.columns([5, 1])
            with col_song:
                song_html = (
                    f'<div class="song-card">🎵 <b>{song_info["title"]}'
                    f"</b> by <i>{song_info['artist']}</i></div>"
                )
                st.markdown(song_html, unsafe_allow_html=True)
            with col_delete:
                if st.button("❌", key=f"delete_{idx}", help="Remove this song"):
                    st.session_state.liked_songs.pop(idx)
                    st.rerun()

    st.markdown("### ➕ Add a New Song")
    col_title, col_artist, col_add = st.columns(
        [2, 2, 0.8], vertical_alignment="center"
    )

    with col_title:
        st.session_state.new_song_title = st.text_input(
            label="Song title",
            value=st.session_state.new_song_title,
            placeholder="Enter song title",
            key="new_title_input",
            label_visibility="collapsed",
        )

    with col_artist:
        st.session_state.new_song_artist = st.text_input(
            label="Artist",
            value=st.session_state.new_song_artist,
            placeholder="Enter artist name",
            key="new_artist_input",
            label_visibility="collapsed",
        )

    with col_add:
        if st.button(
            "➕ Add",
            use_container_width=True,
            disabled=(
                not st.session_state.new_song_title
                or not st.session_state.new_song_artist
            ),
        ):
            st.session_state.liked_songs.append(
                {
                    "title": st.session_state.new_song_title,
                    "artist": st.session_state.new_song_artist,
                }
            )
            st.session_state.new_song_title = ""
            st.session_state.new_song_artist = ""
            st.rerun()


def _get_k_value():
    """Get k value for recommendations, return (k, search_button_pressed)."""
    st.markdown("## 🔍 Get Recommendations", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        k = st.number_input(
            label="Top songs to recommend (k)",
            min_value=1,
            max_value=50,
            value=20,
            label_visibility="collapsed",
        )
    with col2:
        search_button = st.button(
            "🎯 Get Recommendations", use_container_width=True, key="search_button"
        )

    return k, search_button


def _build_liked_songs_objects():
    """Build Song objects from session state liked songs."""
    liked_songs_list = []
    for idx, song_info in enumerate(st.session_state.liked_songs):
        if song_info["title"] and song_info["artist"]:
            liked_songs_list.append(
                Song(
                    id=idx,
                    title=song_info["title"],
                    artist=song_info["artist"],
                )
            )
    return liked_songs_list


def _build_user_object(profile, liked_songs):
    """Build UserProfile object from profile dict and liked songs."""
    return UserProfile(
        id=1,
        name=profile["name"],
        favorite_genre=profile["favorite_genre"],
        favorite_mood=profile["favorite_mood"],
        target_energy=float(profile["target_energy"]),
        likes_acoustic=bool(profile["likes_acoustic"]),
        song_list=liked_songs,
    )


def _discover_songs(api_key, model, user):
    """Discover songs using ArtistDiscoveryService."""
    service = ArtistDiscoveryService(gemini_api_key=api_key, model=model)
    with st.spinner("🔍 Discovering artists and gathering songs..."):
        return service.discover_songs_for_user(
            user,
            artists_per_query=10,
            songs_per_artist=10,
        )


def _display_song_result(rank, song, score, explanation):
    """Display a single song recommendation result."""
    with st.container():
        col_rank, col_song, col_score = st.columns([0.5, 3, 1])
        with col_rank:
            st.markdown(f"### #{rank}")
        with col_song:
            song_info = (
                f"**🎵 {song.title}**\n"
                f"*by {song.artist}*\n"
                f"🏷️ {song.genre} | 😊 {song.mood}\n"
                f"📝 {explanation}"
            )
            st.markdown(song_info)
        with col_score:
            st.metric("Match Score", f"{round(score, 2)}")
        st.divider()


def _handle_recommendations(api_key, model, profile, liked_songs, k):
    """Handle the recommendation discovery and display flow."""
    liked_songs_obj = _build_liked_songs_objects()
    user = _build_user_object(profile, liked_songs_obj)

    st.info(f"🎵 Discovering songs for {user.name}...")

    try:
        songs = _discover_songs(api_key, model, user)

        if not songs:
            st.error("❌ No songs were discovered. Please try different preferences.")
            return

        num_artists = len({s.artist for s in songs})
        st.success(f"✅ Discovered {len(songs)} songs from {num_artists} artists")

        recommender = Recommender(songs)
        results = recommender.recommend(user, k=int(k))

        if not results:
            st.warning("⚠️ No recommendations returned.")
            return

        st.markdown("## 🎵 Your Personalized Recommendations", unsafe_allow_html=True)

        for rank, (song, score, explanation) in enumerate(results, start=1):
            _display_song_result(rank, song, score, explanation)

    except Exception as e:
        st.error(f"❌ Error during discovery: {str(e)}")


def _apply_custom_styling():
    """Apply custom CSS for the app."""
    st.markdown(
        """
        <style>
        .main-header {
            text-align: center;
            color: #1DB954;
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: var(--secondary-text-color, #888);
            font-size: 1.1em;
            margin-bottom: 30px;
        }
        .profile-card {
            border: 2px solid #1DB954;
            border-radius: 10px;
            padding: 20px;
            background-color: transparent;
            margin-bottom: 20px;
            color: inherit;
        }
        .song-card {
            border-left: 4px solid #1DB954;
            padding: 10px;
            background-color: transparent;
            margin: 10px 0;
            border-radius: 5px;
            color: inherit;
        }
        .song-card b { color: inherit; }
        .song-card i { color: inherit; }
        .stColumns > div[role="listitem"] {
            display: flex !important;
            align-items: flex-end !important;
            gap: 0.5rem !important;
        }
        .stTextInput > div, .stNumberInput > div, .stSelectbox > div {
            margin-bottom: 0 !important;
        }
        .stButton > button {
            height: 38px !important;
            margin-top: 0 !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def main():
    """Main application entry point."""
    st.set_page_config(page_title="Find Your Vibe — Recommender", layout="wide")

    _apply_custom_styling()
    _display_header()

    api_key, gemini_model = _validate_api_key()
    if not api_key:
        return

    profile = _get_user_profile()
    _display_liked_songs()
    k, search_button = _get_k_value()

    if search_button:
        # print(k)
        _handle_recommendations(
            api_key, gemini_model, profile, st.session_state.liked_songs, k
        )


if __name__ == "__main__":
    main()
