import os

from src.find_your_vibe.domain.user_preferences import UserProfile
from src.find_your_vibe.services.song_enrichment_service import SongEnrichmentService

# Initialize the enrichment service with optional Gemini API key
# Get this from environment variable or set it directly
gemini_api_key = (
    "AIzaSyDgtlZC7-Rw07OcZFHLS4bcjuxtPJKK8kg"  # os.getenv("GOOGLE_API_KEY")
)
print(f"Using Gemini API key {gemini_api_key}: {'Yes' if gemini_api_key else 'No'}")

service = SongEnrichmentService(gemini_api_key=gemini_api_key)

# Example user profile
user = UserProfile(
    id=1,
    name="Alex",
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.8,
    likes_acoustic=False,
)

# Build multiple search queries from preferences
queries = [
    user.favorite_genre,  # "pop"
    f"{user.favorite_genre} {user.favorite_mood}",  # "pop happy"
    f"{user.favorite_mood} songs",  # "happy songs"
]

# Search for songs using enriched pipeline
all_songs = []
for query in queries:
    print(f"\nSearching for: '{query}'")
    songs = service.search_and_enrich(query=query, limit=10)
    all_songs.extend(songs)
    print(f"  Found {len(songs)} songs")

# Remove duplicates by ID
unique_songs = {song.id: song for song in all_songs}
results = list(unique_songs.values())

print(f"\n✓ Found {len(results)} unique songs matching preferences")
print("\nSample results with audio features:")
for song in results[:5]:
    print(f"  - {song.title} by {song.artist}")
    print(f"    Genre: {song.genre}, Mood: {song.mood}")
    print(
        f"    Energy: {song.energy:.2f}, Danceability: {song.danceability:.2f}, Acousticness: {song.acousticness:.2f}"
    )
