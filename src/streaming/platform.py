"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime, timedelta

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
        self._sessions.append(session)



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
    


# Query methods
# --------------------------------------------------------------------
# Q1: Total Cumulative Listening Time (Return the total cumulative listening time (in minutes)
#  across all users for a given time period. Sum up the listening duration for all sessions that
#  fall within the specified datetime window (inclusive on both ends).)
#----------------------------------------------------------------------------------------------
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        return float(sum(session.duration_listened_seconds / 60 for session in self._sessions
                   if start <= session.timestamp <= end))



# Q2: Average Unique Tracks per Premium User
# Compute the average number of unique tracks listened to per PremiumUser in the last days days 
# (default 30). Only count distinct tracks for sessions within the time window.
# Return 0.0 if there are no premium users.
#----------------------------------------------------------------------------------------------
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        cutoff = datetime.now() - timedelta(days=days)
        premium_count = 0
        total_unique_tracks = 0

        for user in self._users.values():
            if not isinstance(user, PremiumUser):
                continue

            premium_count += 1
            unique_tracks = set()

            for session in self._sessions:
                if session.user == user and session.timestamp >= cutoff:
                    unique_tracks.add(session.track.track_id)

            total_unique_tracks += len(unique_tracks)

        if premium_count == 0:
            return 0.0

        return float(total_unique_tracks / premium_count)    
        
        

# Q3: Track with Most Distinct Listeners
# Return the track with the highest number of distinct listeners (not total plays) in the catalogue.
# Count the number of unique users who have listened to each track and return the one with the most. 
# Return None if no sessions exist.
#----------------------------------------------------------------------------------------------
    def track_with_most_distinct_listeners(self) -> Track | None:
        if len(self.sessions) == 0:
            return None
        
        best_track_id = None
        highest_listener_count = 0

        for track in self._catalogue.values():
            listeners = []
            
            for session in self._sessions:
                if session.track.track_id == track.track_id:
                    if session.user.user_id not in listeners:
                        listeners.append(session.user.user_id)

            if len(listeners) > highest_listener_count:
                highest_listener_count = len(listeners)
                best_track_id = track.track_id

        return self.get_track(best_track_id)



# Q4: Average Session Duration by User Type
# For each user subtype (e.g., FreeUser, PremiumUser, FamilyAccountUser, FamilyMember), 
# compute the average session duration (in seconds) and return them ranked from longest to shortest. 
# Return as a list of (type_name, average_duration_seconds) tuples.
#----------------------------------------------------------------------------------------------
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        totals = {}
        counts = {}

        for session in self._sessions:
            type_name = type(session.user).__name__

            if type_name not in totals:
                totals[type_name] = 0
                counts[type_name] = 0
            
            totals[type_name] += session.duration_listened_seconds
            counts[type_name] += 1
        
        result = []

        for type_name in totals:
            average = totals[type_name] / counts[type_name]
            result.append((type_name, float(average)))

        result.sort(key=lambda x: x[1], reverse=True)
        return result



# Q5: Total Listening Time for Underage Sub-Users
# Return the total listening time (in minutes) attributed to tracks associated with FamilyAccountUser 
# sub-accounts where the sub-account holder (i.e., FamilyMember) is under the specified age threshold 
# (default 18, exclusive). For example, with threshold 18, count only family members with age < 18.
#----------------------------------------------------------------------------------------------
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
            total_seconds = 0

            for session in self._sessions:
                user = session.user

                if isinstance(user, FamilyMember) and user.age < age_threshold:
                    total_seconds += session.duration_listened_seconds

            return float(total_seconds / 60)



# Q6: Top Artists by Listening Time
# Identify the top n artists (default 5) ranked by total cumulative listening time across all their tracks. 
# Only count listening time for tracks where isinstance(track, Song) is true (exclude podcasts and audiobooks). 
# Return as a list of (Artist, total_minutes) tuples, sorted from highest to lowest listening time.
#----------------------------------------------------------------------------------------------
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        artist_totals = {}

        for session in self._sessions:
            track = session.track

            if not isinstance(track, Song):
                continue

            artist_id = track.artist.artist_id

            if artist_id not in artist_totals:
                artist_totals[artist_id] = 0

            artist_totals[artist_id] += session.duration_listened_seconds

        result = []

        for artist_id, total_seconds in artist_totals.items():
            artist = self.get_artist(artist_id)
            total_minutes = total_seconds / 60
            result.append((artist, float(total_minutes)))

        result.sort(key=lambda x: x[1], reverse=True)

        return result[:n]



# Q7: User's Top Genre
# Given a user ID, return their most frequently listened-to genre and the percentage of their total
# listening time it accounts for. Return a (genre, percentage) tuple where percentage is in the range [0, 100],
# or None if the user doesn't exist or has no listening history.
#----------------------------------------------------------------------------------------------
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        user = self.get_user(user_id)

        if user is None:
            return None
    
        genre_totals = {}
        total_seconds = 0

        for session in self._sessions:
            if session.user.user_id != user_id:
                continue

            genre = session.track.genre
            seconds = session.duration_listened_seconds

            if genre not in genre_totals:
                genre_totals[genre] = 0

            genre_totals[genre] += seconds
            total_seconds += seconds
        
        if total_seconds == 0:
            return None
        
        top_genre = None
        most_seconds = 0

        for genre, seconds in genre_totals.items():
            if seconds > most_seconds:
                most_seconds = seconds
                top_genre = genre

        percentage = (most_seconds / total_seconds) * 100

        return (top_genre, float(percentage))



# Q8: Collaborative Playlists with Many Artists
# Return all CollaborativePlaylist instances that contain tracks from more than threshold (default 3) distinct artists.
# Only Song tracks count toward the artist count (exclude Podcast and AudiobookTrack which don't have artists). 
# Return playlists in the order they were registered.
#----------------------------------------------------------------------------------------------
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        result = []

        for playlist in self._playlists.values():
            if not isinstance(playlist, CollaborativePlaylist):
                continue

            artist_ids = set()

            for track in playlist.tracks:
                if isinstance(track, Song):
                    artist_ids.add(track.artist.artist_id)

            if len(artist_ids) > threshold:
                result.append(playlist)

        return result



# Q9: Average Tracks per Playlist Type
# Compute the average number of tracks per playlist, distinguishing between standard Playlist and CollaborativePlaylist instances.
# Return a dictionary with keys "Playlist" and "CollaborativePlaylist" mapped to their respective averages. 
# Return 0.0 for a type with no instances.
#----------------------------------------------------------------------------------------------
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        regular = []
        collaborative = []

        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                collaborative.append(playlist)
            else:
                regular.append(playlist)

        if len(regular) == 0:
            regular_avg = 0.0
        else:
            regular_avg = sum(len(p.tracks) for p in regular) / len(regular)

        if len(collaborative) == 0:
            collaborative_avg = 0.0
        else:
            collaborative_avg = sum(len(p.tracks) for p in collaborative) / len(collaborative)
        
        return {
            "Playlist": float(regular_avg),
            "CollaborativePlaylist": float(collaborative_avg)
        }


# Q10: Users Who Completed Albums
# Identify users who have listened to every track on at least one complete Album and return the corresponding album titles.
# A user "completes" an album if their session history includes at least one listen to each track on that album. 
# Return as a list of (User, [album_title, ...]) tuples in registration order. Albums with no tracks are ignored.
#----------------------------------------------------------------------------------------------
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        result = []

        for user in self._users.values():
            listened_track_ids = {
                session.track.track_id
                for session in self._sessions
                if session.user == user
            }

            completed_albums = []

            for album in self._albums.values():
                if not album.tracks:
                    continue

                if album.track_ids().issubset(listened_track_ids):
                    completed_albums.append(album.title)

            if completed_albums:
                result.append((user, completed_albums))

        return result