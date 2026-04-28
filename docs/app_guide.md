# 🎵 Find Your Vibe — App User Guide

## Overview

**Find Your Vibe** is an interactive Streamlit application that discovers and recommends music tailored to your taste. It combines **Gemini AI** for artist recommendations and **MusicBrainz** for song discovery.

## Quick Start

### 1. Prerequisites
- Python 3.8+
- Gemini API key (free) — [Get one here](https://aistudio.google.com/app/apikey)

### 2. Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Run the App
```bash
# Set your Gemini API key
export GOOGLE_API_KEY="your-api-key-here"

# Start the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## How to Use

### Step 1: Configure Gemini API Key
In the left **Configuration** sidebar:
1. Enter your Gemini API key in the password field
2. Select your preferred Gemini model from the dropdown
3. You'll see a confirmation message when configured

**Models available:**
- `gemini-3.1-flash-lite-preview` (fastest, recommended)
- `gemini-3.1-flash-preview`
- `gemini-2.5-flash`
- `gemini-2.5-flash-lite`



### Step 2: Create Your Profile
Fill in the profile section with your music preferences:

| Field | Example |
|-------|---------|
| **👤 Your Name** | Alex, Jamie, etc. |
| **🎸 Favorite Genre** | pop, rock, jazz, hip-hop, etc. |
| **😊 Favorite Mood** | energetic, calm, happy, sad, etc. |
| **⚡ Target Energy Level** | 0.0 (quiet) to 1.0 (intense), default 0.6 |
| **🎸 Acoustic Preference** | Check if you like acoustic music |
| **🎭 Current Mood** | Select from 10 preset moods (Happy, Sad, Calm, Energetic, etc.) |

### Step 3: Add Your Favorite Songs (Optional)
In the "❤️ Songs You Like" section:

1. Enter a song title in the first field
2. Enter the artist name in the second field
3. Click **➕ Add** to add the song
4. Repeat to add more songs (up to 10)
5. Click **❌** to remove a song

These songs help personalize recommendations based on your history.

### Step 4: Select Number of Recommendations
In the "🔍 Get Recommendations" section:
- Enter how many songs you want recommended (1-50)
- Default is 20

### Step 5: Get Recommendations
Click **🎯 Get Recommendations** to start the discovery:

1. **Discovers:** The app finds artists matching your profile using Gemini
2. **Gathers:** Searches MusicBrainz for ~10 songs per artist
3. **Enriches:** Uses Gemini to infer audio features (energy, mood, danceability, etc.)
4. **Ranks:** Scores each song against your profile and displays top-k recommendations

---

## Understanding Your Recommendations

Each recommended song shows:

```
#1
🎵 Song Title
by Artist Name
🏷️ Genre | 😊 Mood
📝 Explanation (why it matched your profile)
Match Score: 95.25
```

### Match Score Breakdown

The score (0-100) is calculated using:
- **35%** Genre match
- **30%** Mood match
- **20%** Energy match
- **10%** Acoustic preference
- **5%** Danceability

Example:
- **95+** = Perfect match
- **80-95** = Great match
- **70-80** = Good match
- **60-70** = Decent match

---

## Tips for Better Recommendations

### ✅ Do This:
- **Be specific** with genre (e.g., "indie pop" instead of just "pop")
- **Add your liked songs** — the more examples, the better
- **Choose your current mood** — it affects discovery
- **Try different moods** — see how recommendations change

### ❌ Avoid:
- Using generic genres like "music" or "everything"
- Conflicting preferences (e.g., "I like both rap and classical" — try one at a time)
- Very high k values (50+) if you have a slow connection

---

## Example Scenarios

### Scenario 1: Jazz Lover
```
Profile:
- Name: Alex
- Favorite Genre: jazz
- Favorite Mood: relaxed
- Energy: 0.4
- Acoustic: Yes
- Current Mood: Peaceful
- Top k: 5

Result: Smooth jazz standards, acoustic jazz, lounge music
```

### Scenario 2: Gym Motivation
```
Profile:
- Name: Jordan
- Favorite Genre: hip-hop
- Favorite Mood: energetic
- Energy: 0.9
- Acoustic: No
- Current Mood: Energetic
- Liked Songs: [Lose Yourself - Eminem, Till I Collapse - Eminem]
- Top k: 20

Result: High-energy hip-hop, rap, EDM with intense beats
```

### Scenario 3: Late Night Chill
```
Profile:
- Name: Casey
- Favorite Genre: indie
- Favorite Mood: calm
- Energy: 0.3
- Acoustic: Yes
- Current Mood: Calm
- Top k: 10

Result: Indie lo-fi, singer-songwriter, bedroom pop
```

---

## Troubleshooting

### ❌ "Error during discovery"
**Cause:** Gemini API key invalid or rate limit exceeded  
**Solution:**
1. Verify your API key from [aistudio.google.com](https://aistudio.google.com/app/apikey)
2. Wait a few minutes if rate limited
3. Check your internet connection

### ❌ "No songs were discovered"
**Cause:** Your preferences are too specific  
**Solution:**
- Try a more general genre (e.g., "pop" instead of "vaporwave")
- Use common mood descriptors
- Check if the genre exists in MusicBrainz

### ❌ Buttons not aligning / UI looks broken
**Cause:** Browser cache or Streamlit version  
**Solution:**
1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Clear browser cache
3. Try a different browser

### 🐌 App is slow
**Cause:** Large dataset being discovered (~100 songs)  
**Solution:**
- Reduce `songs_per_artist` in the code (default is 10)
- Try a different model (flash models are faster)
- Ask for fewer recommendations (k=5 instead of 20)

---

## Advanced Usage

### Dark Mode
Streamlit automatically detects your OS theme. To explicitly set:
1. Click menu (☰) → Settings
2. Choose Light or Dark theme

### Environment Configuration
Create a `.env` file for persistent settings:
```
GOOGLE_API_KEY=your-key-here
```

Then load it:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Architecture

```
User Input (Profile + Liked Songs)
         ↓
    [GEMINI]
    Recommend 10 artists
         ↓
    [MUSICBRAINZ]
    Discover ~100 songs
         ↓
    [GEMINI]
    Enrich with audio features
         ↓
    [RECOMMENDER]
    Score & rank against profile
         ↓
    Display Top-K Results
```

See [architecture.md](architecture.md) for detailed technical information.

---

## FAQ

**Q: Is my data stored?**  
A: No. All processing happens in your session. Refresh the page to clear everything.

**Q: Can I export recommendations?**  
A: Currently no, but you can take a screenshot. Future version may add CSV export.

**Q: What if I don't have a Gemini API key?**  
A: You can't use the app — the API key is required for AI-powered discovery. Get a free one in 2 minutes at [aistudio.google.com](https://aistudio.google.com/app/apikey).

**Q: Can I use Spotify API instead of MusicBrainz?**  
A: The architecture is pluggable. See [ARCHITECTURE.md](ARCHITECTURE.md) for more details.

**Q: Why do recommendations change each time?**  
A: Gemini's inferences can vary slightly. Run it multiple times on the same profile to see the variation.

---

## Contact & Support

For issues or feature requests:
- Check [troubleshooting](#troubleshooting) section above
- See [gemini_setup.md](gemini_setup.md) for API key issues
- Review [architecture.md](architecture.md) for technical details
