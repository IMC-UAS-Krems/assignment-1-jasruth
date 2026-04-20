"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""



# Artist class & it's methods
#-------------------------------------------------------------------------------------------------------- 
class Artist:
    def __init__(self, artist_id:str, name:str, genre:str, tracks = None):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = tracks if tracks is not None else []

    def add_track(self, track) -> None:
        """add a track to the artists collection"""
        self.tracks.append(track)

    def track_count(self) -> int:
        """returns total number of tracks from an artist"""
        return len(self.tracks)