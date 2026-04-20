"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from datetime import date



# Main class & methods
#-------------------------------------------------------------------------------------------------------- 
class User:
    def __init__(self, user_id:str, name:str, age:int, sessions = None):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = sessions if sessions is not None else []   

    def add_session(self, session) -> None:
        """adds a listened to session to the user"""
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        """Calculates the total listening time in seconds"""
        return sum(session.duration_listened_seconds for session in self.sessions)
    
    def total_listening_minutes(self) -> float:
        """Calcultes total listening time in minutes"""
        return self.total_listening_seconds() / 60
    
    def unique_tracks_listened(self) -> set[str]:
        """gets a set of track ids the user has listened to"""
        return {session.track.track_id for session in self.sessions}


# Subclasses & methods
#-------------------------------------------------------------------------------------------------------- 
class FamilyAccountUser(User):
    def __init__(self, user_id:str, name:str, age:int, sessions = None, sub_users = None):
        super().__init__(user_id, name, age, sessions)
        self.sub_users = sub_users if sub_users is not None else []     

    def add_sub_user(self, sub_user) -> None:
        """add member to the account"""
        self.sub_users.append(sub_user)

    def all_members(self):
        """returns all users in the family account"""
        return [self] + self.sub_users



class FamilyMember(User):
    def __init__(self, user_id:str, name:str, age:int, parent:FamilyAccountUser, sessions = None):
        super().__init__(user_id, name, age, sessions)
        self.parent = parent



class FreeUser(User):
    def __init__(self, user_id, name, age, sessions = None):
        super().__init__(user_id, name, age, sessions)
    MAX_SKIPS_PER_HOUR = 6       



class PremiumUser(User):
    def __init__(self, user_id:str, name:str, age:int, subscription_start:date, sessions = None):
        super().__init__(user_id, name, age, sessions)
        self.subscription_start = subscription_start