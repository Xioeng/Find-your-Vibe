"""Test the full artist-based discovery pipeline.

This script demonstrates:
1. Creating a user profile with preferences
2. Using Gemini to recommend artists based on the profile
3. Discovering singles for each artist via MusicBrainz
4. Enriching songs with audio features
5. Collecting ~100-200 songs for the recommender
"""

import os

from src.find_your_vibe.domain.user_preferences import UserProfile
from src.find_your_vibe.services.artist_discovery_service import (
    ArtistDiscoveryService,
)

# Example user profile
user = UserProfile(
    id=1,
    name="Alex",
    favorite_genre="rock in spanish",
    favorite_mood="happy",
    target_energy=0.8,
    likes_acoustic=False,
    song_list=["Un Sentimiento Muerto en Un Corazon Roto by Porta"],
)

print("=" * 60)
print("🎵 ARTIST-BASED SONG DISCOVERY PIPELINE")
print("=" * 60)

print("\n📋 User Profile:")
print(f"   Name: {user.name}")
print(f"   Genre: {user.favorite_genre}")
print(f"   Mood: {user.favorite_mood}")
print(f"   Energy target: {user.target_energy}")
print(f"   Acoustic preference: {'Yes' if user.likes_acoustic else 'No'}")
if user.song_list:
    print(f"   Recent likes: {', '.join(user.song_list)}")

# Initialize discovery service with optional Gemini API
gemini_api_key = os.getenv("GOOGLE_API_KEY")
model = "gemini-3.1-flash-lite-preview"  # or "gemini-3-flash-preview"
print(gemini_api_key)
# raise Exception("Check Gemini API key configuration")  # --- IGNORE ---

service = ArtistDiscoveryService(gemini_api_key=gemini_api_key, model=model)

# Discover songs: ~10 artists × ~10 songs = ~100 songs
songs = service.discover_songs_for_user(
    user,
    artists_per_query=10,
    songs_per_artist=10,
)

print("\n" + "=" * 60)
print("✅ DISCOVERY COMPLETE")
print("=" * 60)

print("\n📊 Results:")
print(f"   Total songs discovered: {len(songs)}")
