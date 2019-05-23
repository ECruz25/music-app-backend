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

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)

app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# scope = 'user-library-read'
# username = "lbfi9hhe1i06wly52k8996i9s"
# client_id = '5c3b13a967bc4bf598898a7eaac6e54a'
#redirect_uri = 'spotify-app-ec://callback'
#client_secret='de48c9b902314b31a712e838ffe43fa1'

#token = util.prompt_for_user_token(username = username, scope = scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == "GET":
        # return jsonify(get_get_user_tracks())
        
        return "hello from me"
        # return jsonify(get_tracks_by_playlist('lbfi9hhe1i06wly52k8996i9s', get_playlist_by_user('lbfi9hhe1i06wly52k8996i9s')[21]['id']))


def get_playlist_by_user(user_id):
    spotify = spotipy.Spotify(auth=request.form['data']['accessToken'])
    playlists = spotify.user_playlists(user_id)
    return playlists['items']


def get_tracks_by_playlist(user_id, playlist_id):
    tracks = spotify.user_playlist_tracks(user_id, playlist_id)
    for track in tracks['items']:
        print(track)
        SpotifyUserSongInPlaylist(
            user_id, track['added_at'], track['track']['id'], track['track']['popularity'], track['track']['explicit'])
    return tracks


def get_get_user_tracks():
  return spotify.current_user_saved_tracks()


class SpotifyUserSongInPlaylist:
    # __tablename__ = 'spotifyusersonginplaylist'
    # user_id = db.Column(db.String())
    # date_added = db.Column(db.DateTime())
    # track_id = db.Column(db.String())
    # popularity = db.Column(db.Integer())
    # explicit = db.Column(db.Boolean())

    def __init__(self, user_id, date_added, track_id, popularity, explicit):
        self.user_id = user_id
        self.date_added = date_added
        self.track_id = track_id
        self.popularity = popularity
        self.explicit = explicit
