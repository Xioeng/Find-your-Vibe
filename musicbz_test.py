import musicbrainzngs

from src.find_your_vibe.services.spotify_client import MusicBrainzClient

musicbrainzngs.set_useragent("find-your-vibe", "0.1.0", contact="")
artists = musicbrainzngs.search_artists(query="queen", limit=5)
for artist in artists["artist-list"]:
    print(f"{artist['name']} (ID: {artist['id']})")

band = artists["artist-list"][0]
band_id = band["id"]

print(f"\nSearching for releases...")
releases = musicbrainzngs.search_recordings(query="amor y deudas", limit=5)
for release in releases["recording-list"]:
    print(release)
song = releases["recording-list"][0]
song_id = song["id"]

print(f"\nSearching for recordings by {band['name']}...")
recordings = musicbrainzngs.browse_releases(
    artist=band_id,
    release_type=["single"],
    release_status=["official"],
    limit=20,
    offset=0,
)
print(recordings)
for recording in recordings["release-list"]:
    print(f"{recording['title']} (ID: {recording['id']})")

recordings = musicbrainzngs.browse_release_groups(
    # artist=band_id,
    release=song_id,
    release_type=["single"],
    # release_status=["official"],
    limit=20,
    offset=0,
)
print(recordings)
for recording in recordings["release-group-list"]:
    print(f"{recording['title']} (ID: {recording['id']})")


recordings = musicbrainzngs.browse_release_groups(
    # artist=band_id,
    release=song_id,
    release_type=["single"],
    # release_status=["official"],
    limit=20,
    offset=0,
)
print(recordings)
for recording in recordings["release-group-list"]:
    print(f"{recording['title']} (ID: {recording['id']})")
