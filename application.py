
from flask import Flask, request, jsonify, json
import os
from flask_sqlalchemy import SQLAlchemy
import spotipy
import spotipy.util as util
import pycountry
import math
import numpy
import random

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import SpotifyUserSongInPlaylist, User, Playlist

scope = 'user-library-read'
username = "lbfi9hhe1i06wly52k8996i9s"
client_id = '5c3b13a967bc4bf598898a7eaac6e54a'
redirect_uri = 'spotify-app-ec://callback'
client_secret='de48c9b902314b31a712e838ffe43fa1'

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == "GET":
        user_id = 'lbfi9hhe1i06wly52k8996i9s'
        authToken = "BQBsCKenAloVzogTa-psIh0yq69U4kgoPbHNoj3mFBMsoi4yizjWJBAR06LE4tsRdJks5WvieZMLNaPCnGx8t-YW6HSirwkXmEi2nlfsY8SMtfTR6rhZ0c0hkNgoK0NRp7Ffjqy1WMMplucofW1lJU94typ4L-QZKHRN1FwPxix88OyMQCBk-PamMgHF0fNciGMncWnkLsgg_pTwd9Xk"
        mind_aspect = "I"
        energy_aspect = "N"
        nature_aspect = "T"
        tactics_aspect = "J"
        identity_aspect = "T"
        get_all_playlsts(authToken)
        # query = db.session.query(SpotifyUserSongInPlaylist).filter_by(user_id=user_id)
        # # save_tracks_by_playlist(user_id, get_playlist_by_user(user_id)[21]['id'])
        # users = []
        # for song in query:
        #     users.append(song.user_id)

        # if len(users) <= 0:
        #     user = User(user_id, mind_aspect, energy_aspect, nature_aspect, tactics_aspect, identity_aspect)
        #     db.session.add(user)
        #     db.session.commit()
        #     for playlistId in get_playlists_by_user(user_id, authToken):
        #         save_tracks_by_playlist(user_id, playlistId, authToken)
        
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

def get_playlists_by_user(user_id, authToken):
    spotify = spotipy.Spotify(auth=authToken)
    playlists = spotify.user_playlists(user_id)
    playlists_id = []
    offset_amount = math.ceil(playlists['total'] / playlists['limit'])
    for offset in numpy.arange(offset_amount):
        playlists1 = spotify.user_playlists(user_id, offset=offset*playlists['limit'])
        for playlist in playlists1['items']:
            playlists_id.append(playlist['id'])
    return playlists_id

def save_tracks_by_playlist(user_id, playlist_id, authToken):
    spotify = spotipy.Spotify(auth=authToken)
    tracks = spotify.user_playlist_tracks(user_id, playlist_id, offset=100)
    offset_amount = math.ceil(tracks['total'] / tracks['limit'])
    for offset in numpy.arange(offset_amount):
        tracks2 = spotify.user_playlist_tracks(user_id, playlist_id, offset=offset*tracks['limit'])
        for track in tracks2['items']:
            track_ = SpotifyUserSongInPlaylist(
                user_id, track['added_at'], track['track']['id'], track['track']['popularity'], track['track']['explicit'])
            db.session.add(track_)
            db.session.commit()


def get_all_playlsts(authToken):
    spotify = spotipy.Spotify(auth=authToken)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    countries = ['ec', 'fr','ar','fi','no','it','lt','ph','tw','nz','ee','tr','us','sv','cr','de','cl','jp','br','hn','gt','ch','hu','ca','pe','be','my','dk','bo','pl','at','pt','se','mx','pa','uy','is','es','cz','ie','nl','sk','co','sg','id','do','lu','gb','global','py','au','lv','gr','hk']
    mind_aspects = ['E', 'I']
    energy_aspects = ['S', 'N']
    nature_aspects = ['T', 'F']
    tactics_aspects = ['J', 'P']
    identity_aspects = ['A', 'T']
    for i in numpy.arange(len(countries)):
        try:
            print("Started with: " + countries[i])
            for letter in numpy.arange(len(letters)):
                pl = spotify.search(letters[letter],type="playlist", market=countries[i], limit=50)
                offset_amount = math.ceil(pl['playlists']['total'] / pl['playlists']['limit'])
                for offset in numpy.arange(offset_amount):
                    playlists = spotify.search(q=letters[letter],type="playlist", market=countries[i], offset=offset, limit=50)['playlists']['items']
                    for playlist in playlists:
                        if playlist['owner']['id'] != 'spotify':
                            db.session.add(Playlist(playlist_id=playlist['id'], name=playlist['name'], owner=playlist['owner']['id']))
                            db.session.add(User(playlist['owner']['id'], "", "", "", "", "", country=countries[i]))
                            db.session.commit()

        except Exception as e:
            print(e)
        print("finished with country: "+ countries[i-1])