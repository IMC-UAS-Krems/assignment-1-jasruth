"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from streaming.tracks import Track, Song, AlbumTrack, SingleRelease, Podcast, NarrativeEpisode, InterviewEpisode, AudiobookTrack
from streaming.users import User, FamilyAccountUser, FamilyMember, FreeUser, PremiumUser
from streaming.artists import Artist
from streaming.albums import Album
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self._catalogue: dict[str, Track] = {}
        self._users: dict[str, User] = {}
        self._artists: dict[str, Artist] = {}
        self._albums: dict[str, Album] = {}
        self._playlists: dict[str, Playlist] = {}
        self._sessions: list[ListeningSession] = []


# Methods
# -------------------------------------------------------------------
    def add_track(self, track: Track) -> None:
        self._catalogue[track.track_id] = track
        
    def add_user(self, user: User) -> None:
        self._users[user.user_id] = user

    def add_artist(self, artist: Artist) -> None:
        self._artists[artist.artist_id] = artist

    def add_album(self, album: Album) -> None:
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist) -> None:
        self._playlists[playlist.playlist_id] = playlist


# Record session
# -------------------------------------------------------------------
    def record_session(self, session:ListeningSession) -> None:
        self.sessions.append(session)


# get methods
# -------------------------------------------------------------------
    def get_track(self, track_id: str) -> Track | None:
        return self._catalogue.get(track_id)

    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def get_artist(self, artist_id: str) -> Artist | None:
        return self._artists.get(artist_id)

    def get_album(self, album_id: str) -> Album | None:
        return self._albums.get(album_id)


# List methods
# -------------------------------------------------------------------
    def all_users(self) -> list[User]:
        return list(self._users.values())

    def all_tracks(self) -> list[Track]:
        return list(self._catalogue.values())