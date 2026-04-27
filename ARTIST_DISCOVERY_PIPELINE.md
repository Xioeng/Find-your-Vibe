# Artist-Based Discovery Pipeline

## Overview

This pipeline enables your music recommender system to discover and enrich songs at scale by combining **Gemini's intelligence** with **MusicBrainz's music database**.

```
User Profile (preferences + history)
         ↓
    [GEMINI]
    Recommend 10 artists
         ↓
    [MUSICBRAINZ]
    Find 10 singles/artist
    (~100-200 songs total)
         ↓
    [GEMINI]
    Enrich with audio features
         ↓
    Complete Song Objects
    (ready for recommender)
```

## The Pipeline Steps

### Step 1: User Profile Input
```python
user = UserProfile(
    id=1,
    name="Alex",
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.8,
    likes_acoustic=False,
    song_list=["Levitating - Dua Lipa", "Blinding Lights - The Weeknd"]
)
```

### Step 2: Gemini Recommends Artists (10 artists)
**Input**: User profile  
**Process**: Gemini analyzes preferences and suggests matching artists  
**Output**: List of artist names

Example recommendation:
```json
[
    "Taylor Swift",
    "The Weeknd",
    "Ariana Grande",
    "Dua Lipa",
    "Billie Eilish",
    "Post Malone",
    "Ed Sheeran",
    "Harry Styles",
    "Olivia Rodrigo",
    "Khalid"
]
```

### Step 3: MusicBrainz Discovers Singles (10 per artist)
**Input**: Artist names  
**Process**:
1. Search for artist → get MusicBrainz ID
2. Browse release-groups with `release_type=["single"]`
3. Collect song metadata

**Output**: ~100-200 songs with:
- Title
- Artist name
- Artist ID
- Release type

### Step 4: Gemini Enriches with Audio Features
**Input**: Song title + artist  
**Process**: Analyze and infer numerical attributes  
**Output**: Complete Song object with:

| Attribute | Type | Range | Source |
|-----------|------|-------|--------|
| energy | float | 0-1 | Gemini |
| mood | string | "happy", "sad", etc. | Gemini |
| valence | float | 0-1 | Gemini |
| danceability | float | 0-1 | Gemini |
| acousticness | float | 0-1 | Gemini |
| tempo_bpm | int | 60-200 | Gemini |

## Usage

### Basic Example

```python
import os
from src.find_your_vibe.services.artist_discovery_service import (
    ArtistDiscoveryService,
)
from src.find_your_vibe.domain.user_preferences import UserProfile

# Create user profile
user = UserProfile(
    id=1,
    name="Alex",
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.8,
    likes_acoustic=False,
    song_list=["Levitating - Dua Lipa"]
)

# Initialize service (requires optional Gemini API key)
gemini_key = os.getenv("GOOGLE_API_KEY")
service = ArtistDiscoveryService(gemini_api_key=gemini_key)

# Run the pipeline
songs = service.discover_songs_for_user(
    user,
    artists_per_query=10,    # Recommend 10 artists
    songs_per_artist=10      # Get 10 singles per artist
)

# Result: ~100 enriched songs
print(f"Discovered {len(songs)} songs")
```

### Run the Test Script

```bash
# Set your Gemini API key (optional)
export GOOGLE_API_KEY="your-key-here"

# Run the full pipeline
python artist_discovery_test.py
```

## Configuration

### Artist Recommendations

Gemini looks at:
- Favorite genre
- Favorite mood
- Target energy level
- Acoustic preferences
- Past likes (song history)

### Single Songs Filter

MusicBrainz API options used:
```python
musicbrainzngs.browse_release_groups(
    artist=artist_id,
    release_type=["single"],  # ← Filter for singles only
    limit=10
)
```

## Data Flow

```
ArtistDiscoveryService
├── discover_songs_for_user()
│   ├── _recommend_artists()
│   │   ├── Build Gemini prompt from user profile
│   │   ├── Call Gemini API
│   │   ├── Parse JSON artist list
│   │   └── Fallback to genre-based defaults
│   │
│   ├── _discover_artist_singles()  [×10 artists]
│   │   ├── Search MusicBrainz for artist ID
│   │   ├── Browse release groups (singles)
│   │   └── Collect ~10 songs per artist
│   │
│   └── _enrich_song()  [×100-200 songs]
│       ├── Call Gemini to infer features
│       └── Create Song object with all attributes
│
└── Return: list[Song] with complete metadata
```

## Error Handling

### If Gemini API is unavailable:
- 🎯 **Artist recommendations** fall back to genre-based defaults
- ✅ Songs still discovered via MusicBrainz
- 📊 Features default to neutral values (0.5, "neutral", 120 BPM)

### If MusicBrainz fails:
- Returns empty list for that artist
- Continues with other artists
- Logs warning but doesn't crash

## Performance

### API Calls
- **Gemini calls**: ~11-12 (1 for artists + ~1 per artist typically)
- **MusicBrainz calls**: ~20 (search + browse per artist)
- **Total duration**: 5-30 seconds depending on API latency

### Results
- **Artists**: ~10
- **Songs per artist**: ~10 (singles only)
- **Total songs**: ~100-200
- **Memory usage**: ~10KB per enriched song

## Customization

### Change Parameters

```python
# Get more artists, fewer songs
songs = service.discover_songs_for_user(
    user,
    artists_per_query=20,   # More artists
    songs_per_artist=5      # Fewer songs each
)

# Get fewer artists, more songs
songs = service.discover_songs_for_user(
    user,
    artists_per_query=5,    # Fewer artists
    songs_per_artist=20     # More songs each
)
```

### Add Custom Genres

Edit `_default_artists_for_genre()` to add more genres:

```python
defaults = {
    "pop": [...],
    "rock": [...],
    "classical": [
        "Wolfgang Amadeus Mozart",
        "Ludwig van Beethoven",
        # ...
    ]
}
```

### Modify Feature Inference

Edit `_build_feature_inference_prompt()` to change how Gemini analyzes songs.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No artists recommended | Check `GOOGLE_API_KEY` env var |
| Songs found but neutral features | Gemini not configured (still works!) |
| MusicBrainz rate limit (429) | Add delays between artist searches |
| "Artist not found" | Try without special characters |
| Empty release-groups | Artist has no singles in MusicBrainz |

## Next Steps

1. ✅ Run `artist_discovery_test.py` to test pipeline
2. → Integrate discovered songs into recommender
3. → Evaluate song quality for your use case
4. → Adjust parameters (artists_per_query, songs_per_artist)
5. → Monitor API usage and costs

## Files

- **`artist_discovery_service.py`** - Main pipeline orchestrator
- **`artist_discovery_test.py`** - Full pipeline example
- **`llm_analyzer.py`** - Gemini integration
- **`spotify_client.py`** - MusicBrainz integration (used internally)

## Dependencies

- `google.genai` - For Gemini API
- `musicbrainzngs` - For MusicBrainz API
- `dataclasses` - For Song and UserProfile

See `requirements.txt` for versions.
