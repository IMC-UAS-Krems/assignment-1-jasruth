"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""



# Main class & methods
#-------------------------------------------------------------------------------------------------------- 
class Playlist:
    def __init__(self, playlist_id:str, name:str, owner:"User", tracks = None):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = tracks if tracks is not None else []
    
    def add_track(self, track) -> None:
        if track not in self.tracks:
            self.tracks.append(track)
        
    def remove_track(self, track_id) -> None:
        self.tracks = [track for track in self.tracks if track.track_id != track_id]

    def total_duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)



# CollaborativePlaylist subclass & methods
#-------------------------------------------------------------------------------------------------------- 
class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id:str, name:str, owner:"User", tracks = None, contributors = None):
        super().__init__(playlist_id, name, owner, tracks)
        self.contributors = contributors if contributors is not None else [owner]

    def add_contributor(self, user) -> None:
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user) -> None:
        if user is not self.owner and user in self.contributors:
            self.contributors.remove(user)