# Gemini API Setup Guide

## Overview

The music recommender system now uses **Google Generative AI (Gemini)** to intelligently infer audio features (energy, mood, acousticness, danceability, tempo) for songs discovered via MusicBrainz.

## Quick Start

### 1. Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Select your project (or create a new one)
4. Copy your API key

### 2. Set the Environment Variable

**Option A: Local Development**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

**Option B: Windows Command Prompt**
```cmd
set GOOGLE_API_KEY=your-api-key-here
```

**Option C: In Python code**
```python
import os
os.environ["GOOGLE_API_KEY"] = "your-api-key-here"
```

**Option D: .env file** (recommended for projects)
Create a `.env` file in your project root:
```
GOOGLE_API_KEY=your-api-key-here
```

Then load it in your code:
```python
from dotenv import load_dotenv
import os

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `google-generativeai` which is required.

### 4. Run Your Application

```bash
python client_test.py
```

## How It Works

```
User Search Query
       ↓
  MusicBrainz API
  (Find songs)
       ↓
[Song Title + Artist]
       ↓
  Gemini API
  (Infer audio features)
       ↓
[Complete Song with features:
 - energy, mood, valence
 - danceability, acousticness
 - tempo_bpm]
```

## What Gemini Infers

Gemini analyzes the song title and artist to estimate:

| Feature | Range | Meaning |
|---------|-------|----------|
| **energy** | 0-1 | How intense/powerful (0=quiet, 1=intense) |
| **mood** | String | happy, sad, energetic, calm, melancholic, etc. |
| **valence** | 0-1 | Musical positiveness (0=sad, 1=happy) |
| **danceability** | 0-1 | How suitable for dancing |
| **acousticness** | 0-1 | Acoustic vs electronic (0=electric, 1=acoustic) |
| **tempo_bpm** | 60-200 | Estimated beats per minute |

## Fallback Behavior

If the Gemini API is unavailable (no key or API error):
- Songs are still discovered via MusicBrainz
- Audio features default to neutral values (0.5, "neutral", 120 BPM, etc.)
- No search is blocked - the app continues to work

## Price & Limits

- **Gemini 1.5 Flash**: Free tier includes 15 requests per minute
- See [Gemini API pricing](https://aistudio.google.com/pricing) for limits
- Each song search typically makes 1 Gemini call per song found

## Troubleshooting

### Error: "API key not valid"
- Verify your key is copied correctly
- Check it's set in the right environment variable
- Try generating a new key in Google AI Studio

### Error: "RESOURCE_EXHAUSTED" (quota exceeded)
- You've hit your free tier limit
- Wait a moment and retry
- Upgrade to paid tier if needed

### Songs found but features are neutral
- Gemini API is not configured
- Check your `GOOGLE_API_KEY` environment variable
- The app still works fine with neutral defaults

## Example Usage

```python
import os
from src.find_your_vibe.services.song_enrichment_service import SongEnrichmentService

# Initialize with your API key
gemini_key = os.getenv("GOOGLE_API_KEY")
service = SongEnrichmentService(gemini_api_key=gemini_key)

# Search and enrich songs
songs = service.search_and_enrich(query="upbeat pop", limit=10)

for song in songs:
    print(f"{song.title} by {song.artist}")
    print(f"  Energy: {song.energy:.2f}")
    print(f"  Mood: {song.mood}")
    print(f"  Danceability: {song.danceability:.2f}")
```

## Next Steps

- Try the example in `client_test.py`
- Integrate with your recommender algorithm
- Test with different search queries
- Monitor API usage in [Google AI Studio](https://aistudio.google.com/app/dashboard)
