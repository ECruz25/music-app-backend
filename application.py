from flask import Flask, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import spotipy
import spotipy.util as util
# spotifyusersonginplaylist

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['postgresql://postgres@127.0.0.1:5432/music-app-ec']


# scope = 'user-library-read'
# spotify = spotipy.Spotify()
# util.prompt_for_user_token(username, scope, client_id='5c3b13a967bc4bf598898a7eaac6e54a',
#                            client_secret='de48c9b902314b31a712e838ffe43fa1', redirect_uri='spotify-app-ec://callback')
spotify = spotipy.Spotify(
    auth="BQA4u1sAYbQjc0ZXQvgSA4ikyXMPEOpBSSpOsRHWm82zSzxujqAAiG0UShTFz2DClPsbLvE7YOXk9f6HUjGusdausB6-LiR1oeJLWOC9NiJXbKlP8OCJys3bO4nLzf_-hQC1p6D8BwKhXZu6ZYx0Zg_wYcktiiS2W6EGj04qnuosSjLY8uQVvLOegyxJWoE6QIRwiyc")


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == "GET":
        # return jsonify(get_playlist_by_user('lbfi9hhe1i06wly52k8996i9s')[21]['name'])
        return jsonify(get_tracks_by_playlist('lbfi9hhe1i06wly52k8996i9s', get_playlist_by_user('lbfi9hhe1i06wly52k8996i9s')[21]['id']))


def get_playlist_by_user(user_id):
    playlists = spotify.user_playlists(user_id)
    return playlists['items']


def get_tracks_by_playlist(user_id, playlist_id):
    tracks = spotify.user_playlist_tracks(user_id, playlist_id)
    for track in tracks['items']:
        print(track)
        SpotifyUserSongInPlaylist(
            user_id, track['added_at'], track['track']['id'], track['track']['popularity'], track['track']['explicit'])

    return tracks


class SpotifyUserSongInPlaylist:
    __tablename__ = 'spotifyusersonginplaylist'
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
