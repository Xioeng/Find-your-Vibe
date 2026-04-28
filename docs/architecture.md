# 🏗️ System Architecture & Discovery Pipeline

## Overview

The music recommender system uses a **two-layer architecture** that combines AI-powered artist discovery with intelligent audio feature inference.

```
User Preferences
    ↓
User Profile (genre, mood, energy, acoustic preference, liked songs)
    ↓
┌─────────────────────────────────────────────────────┐
│      ARTIST DISCOVERY & ENRICHMENT PIPELINE         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. [GEMINI] Recommend 10 artists                  │
│     (based on user profile)                        │
│              ↓                                      │
│  2. [MUSICBRAINZ] Discover ~10 songs per artist   │
│     (from singles & singles)                       │
│              ↓                                      │
│  3. [GEMINI] Enrich with audio features            │
│     (infer energy, mood, danceability, etc.)       │
│              ↓                                      │
│  4. Complete Song Objects                          │
│     (ready for recommendation)                      │
│                                                     │
└─────────────────────────────────────────────────────┘
    ↓
[RECOMMENDATION ENGINE]
    Score each song against user profile
    Sort by score (descending)
    Return top-K songs
    ↓
Display Results with Explanations
```

---

## Component Architecture

### Layer 1: Artist Discovery (Gemini)

**What it does:** Recommends relevant artists based on user profile  
**Input:** UserProfile object  
**Output:** List of 10 artist names

**How it works:**
```
Gemini analyzes:
  - Favorite genre
  - Favorite mood
  - Target energy level
  - Acoustic preferences
  - Liked songs (song history)

→ Generates list of matching artists
```

**Example prompt to Gemini:**
```
You are a music curator. Given a user with these preferences:
- Genre: jazz
- Mood: relaxed
- Energy: 0.4 (low)
- Acoustic: yes
- Liked songs: Kind of Blue - Miles Davis

Recommend 10 artists they would enjoy.
Return ONLY a JSON array of artist names.
```

**Example output:**
```json
["John Coltrane", "Thelonious Monk", "Bill Evans", "Chet Baker", ...]
```

### Layer 2: Song Discovery (MusicBrainz)

**What it does:** Finds songs for each recommended artist  
**Input:** Artist names  
**Output:** ~100-200 basic Song objects (title, artist, genre)

**How it works:**
```python
For each artist:
  1. Search MusicBrainz API for artist by name
  2. Get MusicBrainz artist ID
  3. Browse release-groups with type="single"
  4. Collect song metadata

Total: ~10 songs/artist × 10 artists = ~100 songs
```

**MusicBrainz API calls:**
```python
# Step 1: Find artist
artist = musicbrainzngs.search_artists(artist="Miles Davis")

# Step 2: List their singles
releases = musicbrainzngs.browse_release_groups(
    artist=artist_id,
    release_type="single",
    limit=10
)

# Step 3: Extract song information
for release in releases:
    songs.append({
        "title": release["title"],
        "artist": artist["name"],
        "genre": release.get("tag", [{}])[0].get("name", "unknown")
    })
```

### Layer 3: Audio Feature Enrichment (Gemini)

**What it does:** Infers quantitative audio features from song metadata  
**Input:** Song title + artist  
**Output:** Complete Song object with numerical features

**Features inferred:**

| Feature | Range | Meaning | Example |
|---------|-------|---------|---------|
| **energy** | 0-1 | Intensity/power | 0.8 = intense, 0.3 = quiet |
| **mood** | String | Emotional tone | "happy", "melancholic", "energetic" |
| **valence** | 0-1 | Musical positiveness | 0.9 = happy, 0.2 = sad |
| **danceability** | 0-1 | Rhythmic suitability | 0.95 = highly danceable |
| **acousticness** | 0-1 | Acoustic vs electronic | 1.0 = fully acoustic, 0.0 = electronic |
| **tempo_bpm** | 60-200 | Beats per minute | 120 = moderate, 180 = fast |

**How inference works:**
```
Gemini prompt:
"Based on the title and artist, estimate the audio features for:
Song: Levitating
Artist: Dua Lipa

Return JSON with:
{energy: float, mood: string, valence: float, ...}"

Gemini response:
{
  "energy": 0.85,
  "mood": "uplifting",
  "valence": 0.9,
  "danceability": 0.95,
  "acousticness": 0.0,
  "tempo_bpm": 128
}
```

### Layer 4: Recommendation Engine

**What it does:** Ranks songs against user profile  
**Input:** Complete songs + user profile  
**Output:** Top-K recommendations with scores

**Scoring formula:**

```
Score(song, user) = 100 × [
    0.35 × G(song, user) +
    0.30 × M(song, user) +
    0.20 × E(song, user) +
    0.10 × A(song, user) +
    0.05 × D(song)
]
```

Where:
- **G(s,u)** = Genre match: 1.0 if exact, 0.5 otherwise
- **M(s,u)** = Mood match: 1.0 if matches user's favorite mood, 0.5 otherwise
- **E(s,u)** = Energy match: 1 - min(|song.energy - user.energy|, 0.5)
- **A(s,u)** = Acoustic: song.acousticness if user likes acoustic, else 1 - acousticness
- **D(s)** = Danceability: song.danceability value

**Example calculation:**
```
Song: "Levitating" by Dua Lipa
User: Loves pop, energetic, energy 0.8, likes acoustic songs

Features:
  genre_match: 1.0 (pop = pop)
  mood_match: 1.0 (energetic = energetic)
  energy_match: 0.95 (|0.85 - 0.8| = 0.05, 1 - 0.05 = 0.95)
  acoustic: 0.0 (song is not acoustic, but user doesn't like acoustic → 1 - 0.0 = 1.0)
  danceability: 0.95

Score = 100 × [0.35(1.0) + 0.30(1.0) + 0.20(0.95) + 0.10(1.0) + 0.05(0.95)]
      = 100 × [0.35 + 0.30 + 0.19 + 0.10 + 0.047]
      = 100 × 0.987
      = 98.7 ✓ Excellent match!
```

---

## Data Flow Example

### Complete End-to-End Flow

```
INPUT: Jazz Lover Profile
├─ name: "Alex"
├─ favorite_genre: "jazz"
├─ favorite_mood: "relaxed"
├─ target_energy: 0.4
├─ likes_acoustic: true
└─ song_list: ["Kind of Blue - Miles Davis"]

STEP 1: Artist Discovery (Gemini)
│
├─ Gemini receives profile
├─ Analyzes: "Jazz + relaxed + low energy + acoustic-loving"
└─ Output: ["John Coltrane", "Bill Evans", "Thelonious Monk", ...]

STEP 2: Song Discovery (MusicBrainz)
│
├─ Search MusicBrainz for each artist
├─ Find ~10 singles per artist
└─ Output: ~100 basic song objects
   ├─ "Blue Train" by John Coltrane
   ├─ "Autumn Leaves" by Bill Evans
   ├─ "Round Midnight" by Thelonious Monk
   └─ ... more songs

STEP 3: Audio Enrichment (Gemini)
│
├─ For each of ~100 songs:
│  ├─ Send [title, artist] to Gemini
│  └─ Get back features: energy, mood, valence, danceability, etc.
└─ Output: ~100 complete Song objects
   ├─ Song(title="Blue Train", artist="John Coltrane",
   │        energy=0.5, mood="melancholic", valence=0.4, ...)
   └─ ... more enriched songs

STEP 4: Recommendation Ranking
│
├─ For each song, calculate score:
│  ├─ Genre: jazz = jazz? ✓ (match!)
│  ├─ Mood: melancholic ≈ relaxed? ~ (partial)
│  ├─ Energy: 0.5 vs target 0.4? ~ (close)
│  ├─ Acoustic: 0.8 vs prefers acoustic? ✓ (high)
│  └─ Danceability: 0.3? (less weight)
├─ Sort by score (highest first)
└─ Output: Top 5 recommendations

FINAL OUTPUT:
│
├─ #1: "Blue Train" - John Coltrane (Score: 92.5)
├─ #2: "Autumn Leaves" - Bill Evans (Score: 91.0)
├─ #3: "Ballad of a Thin Man" - Live Piano (Score: 88.3)
├─ #4: "Night and Day" - Chet Baker (Score: 87.1)
└─ #5: "Round Midnight" - Thelonious Monk (Score: 86.0)
```

---

## Configuration & Parameters

### Artist Discovery Parameters
```python
service.discover_songs_for_user(
    user=profile,
    artists_per_query=10,      # How many artists to recommend
    songs_per_artist=10        # How many songs per artist
)

# Total songs = artists_per_query × songs_per_artist
# Default: 10 × 10 = ~100 songs
```

### Recommendation Parameters
```python
recommender = Recommender(songs)
results = recommender.recommend(user, k=20)

# k = number of recommendations to return
# Returns top k songs sorted by score
```

### Scoring Weights
Edit in `src/find_your_vibe/recommender/scoring_algorithms.py`:
```python
weights = {
    'genre': 0.35,        # ← Increase to favor genre matches
    'mood': 0.30,         # ← Increase to favor mood matches
    'energy': 0.20,       # ← Increase to favor energy matches
    'acoustic': 0.10,
    'danceability': 0.05,
}
```

---

## External APIs

### Gemini API (Google)

**Purpose:** Artist recommendations & audio feature inference  
**Free tier:** 15 requests/minute  
**Setup:** See [GEMINI_SETUP.md](GEMINI_SETUP.md)

```python
import google.genai as genai

client = genai.Client(api_key="your-key")
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Recommend 10 jazz artists..."
)
```

### MusicBrainz API

**Purpose:** Song discovery  
**Authentication:** None required  
**Rate limit:** 1 request/second (built-in delays)
**Setup:** `pip install musicbrainzngs`

```python
import musicbrainzngs

musicbrainzngs.set_useragent("MyApp/1.0")
results = musicbrainzngs.search_artists(artist="Miles Davis")
```

---

## Error Handling & Fallbacks

The system gracefully handles API failures:

### Gemini Unavailable
```
User asks for recommendations
  ↓
Gemini API fails
  ↓
Use sensible defaults for audio features:
  ├─ energy: 0.5 (neutral)
  ├─ mood: "neutral"
  ├─ danceability: 0.5
  └─ ... (all 0.5 or neutral)
  ↓
Still provide recommendations (with asterisk noting inferred defaults)
```

### MusicBrainz Unavailable
```
Artist search fails
  ↓
Skip that artist, move to next
  ↓
Return whatever songs were successfully found
  ↓
If no songs found at all, show error message
```

---

## Future Improvements

### Plugin Architecture
```python
# Currently: MusicBrainz for discovery
# Future: Pluggable discovery services
class SongDiscoveryService(ABC):
    def discover(self, artists: List[str]) -> List[Song]:
        pass

# Implementations:
# - MusicBrainzDiscovery (current)
# - SpotifyDiscovery (requires auth)
# - LastfmDiscovery (community database)
```

### Caching Layer
```python
# Cache Gemini responses to reduce API calls
cache = {}
cache_key = f"{song.title}|{song.artist}"
if cache_key in cache:
    features = cache[cache_key]
else:
    features = gemini.infer(song)
    cache[cache_key] = features
```

### User Feedback Loop
```python
# Learn from user feedback
recommend(user, k=5)
# User rates recommendations
# System learns weights adjustment
```

---

## Performance Metrics

### Typical Timings (with Gemini API)
```
Artist Discovery:     2-3 seconds   (1 Gemini call)
Song Discovery:       5-10 seconds  (~100 MusicBrainz calls)
Feature Enrichment:   30-60 seconds (~100 Gemini calls)
Recommendation:       <1 second     (scoring only)
─────────────────────────────────
Total:                40-75 seconds per search
```

### Optimization Tips
- Reduce `artists_per_query` from 10 to 5-7
- Use faster Gemini model (flash vs pro)
- Implement caching for repeated searches
- Use batch Gemini calls where possible

---

## Testing

See [app_guide.md](app_guide.md) for user-facing scenarios.

For technical testing:
```bash
# Run test suite
pytest tests/

# Test artist discovery pipeline
python test_scripts/artist_discovery_test.py

# Test recommender scoring
python -m pytest tests/test_recommender.py -v
```

---

## References

- [Gemini API Docs](https://ai.google.dev/)
- [MusicBrainz API Docs](https://musicbrainz.org/doc/MusicBrainz_API)
- [Spotify Audio Features](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features) (reference for feature definitions)
- [gemini_setup.md](gemini_setup.md) — API key configuration
