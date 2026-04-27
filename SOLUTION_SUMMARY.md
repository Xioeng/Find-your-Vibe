# Music Recommender System - API Solution Summary

## Problem Statement
Your music recommender system had two critical challenges:
1. ❌ Spotify API doesn't allow easy song discovery without complex authentication
2. ❌ Available music APIs (like MusicBrainz) don't provide audio features (energy, mood, acousticness, etc.)

## Solution Implemented
A **two-layer architecture** that separates concerns:

### Layer 1: Song Discovery (MusicBrainz)
- ✅ **No authentication required**
- ✅ Reliable and stable API
- ✅ Returns basic metadata: title, artist, ID

### Layer 2: Feature Enrichment (Google Gemini)
- ✅ **Infers audio features** from song name + artist
- ✅ Generates realistic values for: energy, mood, valence, danceability, acousticness, tempo
- ✅ **Free tier available** (15 requests/minute)
- ✅ Graceful degradation if API unavailable

## Architecture Diagram

```
User Preferences
    ↓
Search Query ("upbeat pop")
    ↓
┌─────────────────────────────────┐
│   SongEnrichmentService         │
├─────────────────────────────────┤
│                                 │
│  ┌──────────────────────┐       │
│  │  MusicBrainzClient   │       │
│  │  (Song Discovery)    │       │
│  └──────────────────────┘       │
│         ↓ Find songs            │
│    [Title, Artist, ID]          │
│         ↓                       │
│  ┌──────────────────────┐       │
│  │  GeminiAnalyzer      │       │
│  │  (Feature Inference) │       │
│  └──────────────────────┘       │
│    Analyze: title + artist      │
│         ↓                       │
└─────────────────────────────────┘
    [Complete Song Objects]
         ↓
   energy: 0.8
   mood: "energetic"
   danceability: 0.9
   acousticness: 0.1
   valence: 0.8
   tempo_bpm: 130
```

## Files Modified/Created

### New Files
1. **`GEMINI_SETUP.md`** - Complete guide for setting up Gemini API
2. **`src/find_your_vibe/services/song_enrichment_service.py`** - Main orchestration service

### Modified Files
1. **`src/find_your_vibe/services/llm_analyzer.py`**
   - Added `infer_audio_features()` method
   - Implements Gemini API integration
   - Added `AudioFeatures` dataclass

2. **`src/find_your_vibe/services/__init__.py`**
   - Exported new classes and services

3. **`client_test.py`**
   - Updated to use new `SongEnrichmentService`
   - Demonstrates how to search and display enriched songs

4. **`requirements.txt`**
   - Added `google-generativeai` dependency

## Key Features

### ✅ Robust Error Handling
- If Gemini API is unavailable → uses sensible defaults
- If MusicBrainz fails → returns empty list (no crash)
- Graceful degradation keeps app functional

### ✅ Efficient API Usage
- Only calls Gemini once per song found
- Caches features in Song objects
- Batch processing support

### ✅ Production Ready
- Type hints throughout
- Proper error handling
- Configurable API keys via environment variables
- Clear separation of concerns

### ✅ Flexible Configuration
```python
# Option 1: Environment variable
gemini_key = os.getenv("GOOGLE_API_KEY")

# Option 2: Direct parameter
service = SongEnrichmentService(gemini_api_key="key-here")

# Option 3: No key (uses defaults)
service = SongEnrichmentService()  # Works, but features are neutral
```

## Quick Start

### 1. Get Gemini API Key
Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) and create a free key

### 2. Set Environment Variable
```bash
export GOOGLE_API_KEY="your-key-here"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Example
```bash
python client_test.py
```

## Usage Example

```python
import os
from src.find_your_vibe.services.song_enrichment_service import SongEnrichmentService

# Initialize service with your Gemini API key
gemini_key = os.getenv("GOOGLE_API_KEY")
service = SongEnrichmentService(gemini_api_key=gemini_key)

# Search and get enriched songs
songs = service.search_and_enrich(
    query="happy pop music",
    limit=10
)

# Use the complete Song objects with all features
for song in songs:
    print(f"{song.title} by {song.artist}")
    print(f"  Mood: {song.mood}")
    print(f"  Energy: {song.energy}")
    print(f"  Danceability: {song.danceability}")
    print(f"  Acousticness: {song.acousticness}")
```

## Feature Inference Examples

### Example 1: "Levitating" by Dua Lipa
```
Input:  song_title="Levitating", artist="Dua Lipa"
Output: {
    "energy": 0.8,
    "mood": "energetic",
    "valence": 0.9,
    "danceability": 0.95,
    "acousticness": 0.0,
    "tempo_bpm": 128
}
```

### Example 2: "Imagine" by John Lennon
```
Input:  song_title="Imagine", artist="John Lennon"
Output: {
    "energy": 0.4,
    "mood": "calm",
    "valence": 0.7,
    "danceability": 0.2,
    "acousticness": 0.8,
    "tempo_bpm": 80
}
```

## API Pricing & Limits

| Metric | Free Tier | Paid Tier |
|--------|-----------|-----------|
| **Requests/min** | 15 | 600+ |
| **Monthly Cost** | $0 | $0.01-0.10 per 1K tokens |
| **Best For** | Development/Testing | Production |

See [Google AI Pricing](https://aistudio.google.com/pricing)

## Next Steps

1. ✅ Set up Gemini API key (see `GEMINI_SETUP.md`)
2. ✅ Test with `python client_test.py`
3. → Integrate with your recommender algorithm
4. → Add more search query varieties
5. → Monitor API usage and adjust as needed

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not valid" | Check key in `GOOGLE_API_KEY` env var |
| Songs found but neutral features | Gemini not configured, but app works fine |
| "RESOURCE_EXHAUSTED" | Hit free tier limit, wait or upgrade |
| MusicBrainz rate limits | Use different query terms or add delays |

## Support

- Gemini API docs: [https://aistudio.google.com/](https://aistudio.google.com/)
- MusicBrainz docs: [https://musicbrainzngs.readthedocs.io/](https://musicbrainzngs.readthedocs.io/)
- Song dataclass: [domain/song.py](domain/song.py)
