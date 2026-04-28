# 🎵 Find Your Vibe — Music Recommender System

> **Discover personalized music recommendations powered by AI**

An intelligent music recommendation system that combines **Gemini AI** for artist discovery and **MusicBrainz** for song sourcing. The Streamlit app makes it interactive and easy to use.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 🎤 **AI-Powered Discovery** — Gemini recommends artists based on your preferences
- 🎵 **Automatic Enrichment** — Infer audio features (energy, mood, danceability) intelligently
- 🎯 **Smart Scoring** — Multi-factor recommendation algorithm balancing genre, mood, energy, and more
- 🌙 **Dark Mode Support** — Beautiful UI that works in light and dark themes
- 🚀 **Fast & Lightweight** — No heavy dependencies, pure Python
- 🔌 **Modular Architecture** — Easy to extend and customize

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Free Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

### Installation

```bash
# Navigate to the project
cd MusicRecommenderSimulator

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key
export GOOGLE_API_KEY="your-api-key-here"

# Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 📖 Documentation

### For App Users
- **[🎵 App User Guide](docs/app_guide.md)** — How to use the Streamlit app with examples and troubleshooting

### For Developers
- **[🏗️ System Architecture](docs/architecture.md)** — Technical deep-dive into the recommendation engine and discovery pipeline
- **[🔑 Gemini API Setup](docs/gemini_setup.md)** — Complete guide for configuring the Gemini API

---

## 🎯 How It Works

```
User Profile (Genre, Mood, Energy, Liked Songs)
         ↓
✨ Gemini Recommends 10 Artists
         ↓
🎵 MusicBrainz Discovers ~100 Songs
         ↓
✨ Gemini Enriches with Audio Features
         ↓
🎯 Recommendation Engine Ranks Songs
         ↓
📊 Display Top-K Recommendations
```

For detailed architecture, see **[System Architecture](docs/architecture.md)**.

---

## 🧮 Scoring Algorithm

The recommendation score balances multiple factors:

```
Score(song, user) = 100 × [
    0.35 × Genre Match      +
    0.30 × Mood Match       +
    0.20 × Energy Match     +
    0.10 × Acoustic Pref    +
    0.05 × Danceability
]
```

---

## 📁 Project Structure

```
MusicRecommenderSimulator/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
├── data/
│   └── songs.csv                  # Song database (optional)
├── src/
│   └── find_your_vibe/
│       ├── domain/                # Data models
│       │   ├── song.py
│       │   └── user_preferences.py
│       ├── recommender/           # Recommendation engine
│       │   ├── recommender.py
│       │   └── scoring_algorithms.py
│       └── services/              # External integrations
│           ├── artist_discovery_service.py
│           ├── llm_analyzer.py
│           └── song_enrichment_service.py
├── test_scripts/                   # Example usage
│   └── artist_discovery_test.py
├── tests/                          # Unit tests
│   ├── test_recommender.py
│   └── test_song.py
└── docs/
    ├── APP_GUIDE.md              # User guide
    ├── ARCHITECTURE.md           # System design
    └── GEMINI_SETUP.md          # API setup
```

---

## 🔑 Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Select or create a Google Cloud project
4. Copy your API key
5. Set environment variable:
   ```bash
   export GOOGLE_API_KEY="your-key-here"
   ```

See **[gemini_setup.md](docs/gemini_setup.md)** for detailed instructions.

---

## 🎮 Example Usage

### Via Streamlit App (Recommended)
```bash
streamlit run app.py
```
Then fill in your profile and click "Get Recommendations"

### Via Python Script
```python
import os
from src.find_your_vibe.domain.user_preferences import UserProfile
from src.find_your_vibe.services.artist_discovery_service import ArtistDiscoveryService
from src.find_your_vibe.recommender.recommender import Recommender

# Create profile
user = UserProfile(
    id=1,
    name="Alex",
    favorite_genre="jazz",
    favorite_mood="relaxed",
    target_energy=0.4,
    likes_acoustic=True
)

# Discover and recommend
gemini_key = os.getenv("GOOGLE_API_KEY")
service = ArtistDiscoveryService(gemini_api_key=gemini_key)
songs = service.discover_songs_for_user(user, artists_per_query=10, songs_per_artist=10)

# Get recommendations
recommender = Recommender(songs)
results = recommender.recommend(user, k=5)

# Display
for rank, (song, score, explanation) in enumerate(results, 1):
    print(f"{rank}. {song.title} by {song.artist} (Score: {score:.2f})")
```

---

## 🧪 Testing

Run the test suite:
```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_recommender.py -v
```

Test the artist discovery pipeline:
```bash
python test_scripts/artist_discovery_test.py
```

---

## 🐛 Troubleshooting

### "Error during discovery"
- ✅ Check your Gemini API key is valid
- ✅ Verify internet connection
- ✅ Check if API rate limit exceeded (wait 60s)

### "No songs were discovered"
- ✅ Try a more common genre (e.g., "pop" instead of "vaporwave")
- ✅ Use standard mood descriptors
- ✅ Reduce parameters in code

For more help, see **[app_guide.md — Troubleshooting](docs/app_guide.md#troubleshooting)**.

---

## 📊 Performance

Typical timing (Gemini API + MusicBrainz):
- Artist Discovery: 2-3 seconds
- Song Discovery: 5-10 seconds
- Feature Enrichment: 30-60 seconds
- Scoring: <1 second
- **Total: 40-75 seconds**

💡 **Tip:** Use faster models (flash) for quicker results.

---

## 🔗 Quick Links

| Link | Purpose |
|------|---------|
| [🎵 App Guide](docs/app_guide.md) | How to use the app |
| [🏗️ Architecture](docs/architecture.md) | Technical details |
| [🔑 Gemini Setup](docs/gemini_setup.md) | API configuration |
| [Google AI Studio](https://aistudio.google.com/app/apikey) | Get API key |
| [MusicBrainz](https://musicbrainz.org/) | Music database |

---

## 📝 License

MIT License

---

**Enjoy discovering your next favorite song! 🎵**
