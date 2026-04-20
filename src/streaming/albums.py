"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""



# Album class & methods
#-------------------------------------------------------------------------------------------------------- 
class Album:
    def __init__(self, album_id:str, title:str, artist:"Artist", release_year:int, tracks = None):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = tracks if tracks is not None else []
    
    def add_track(self, track) -> None:
        """Add a track to the album"""
        track.album = self
        self.tracks.append(track)
        self.tracks.sort(key=lambda t: t.track_number)

    def track_ids(self) -> set[str]:
        """Returns a set of all track ids in the album"""
        return {track.track_id for track in self.tracks}
    
    def duration_seconds(self) -> int:
        """Calculates the duration of the album in seconds"""
        return sum(track.duration_seconds for track in self.tracks)