from application import db
from sqlalchemy.dialects.postgresql import JSON

class SpotifyUserSongInPlaylist(db.Model):
    __tablename__ = 'spotifyusersonginplaylist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String())
    date_added = db.Column(db.DateTime())
    track_id = db.Column(db.String())
    popularity = db.Column(db.Integer())
    explicit = db.Column(db.Boolean())

    def __init__(self, user_id, date_added, track_id, popularity, explicit):
        self.user_id = user_id
        self.date_added = date_added
        self.track_id = track_id
        self.popularity = popularity
        self.explicit = explicit


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String())
    mind_aspect = db.Column(db.String(), nullable=True)
    energy_aspect = db.Column(db.String(), nullable=True)
    nature_aspect = db.Column(db.String(), nullable=True)
    tactics_aspect = db.Column(db.String(), nullable=True)
    identity_aspect = db.Column(db.String(), nullable=True)
    country = db.Column(db.String())

    def __init__(self, user_id, mind_aspect, energy_aspect, nature_aspect, tactics_aspect, identity_aspect, country):
        self.user_id = user_id
        self.identity_aspect = identity_aspect
        self.tactics_aspect = tactics_aspect
        self.nature_aspect = nature_aspect
        self.mind_aspect = mind_aspect
        self.energy_aspect = energy_aspect
        self.country = country

class Playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.String())
    name = db.Column(db.String())
    owner = db.Column(db.String())
    checked = db.Column(db.Boolean())

    def __init__(self, playlist_id, name, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.checked = False