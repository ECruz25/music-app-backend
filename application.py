from flask import Flask, request, jsonify, json
from datetime import date

import os
from flask_sqlalchemy import SQLAlchemy
import spotipy
import spotipy.util as util
import math
import numpy
import random
import pandas as pd
from collections import defaultdict

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import SpotifyUserSongInPlaylist, User, Playlist, Recommendation

scope = 'user-library-read'
username = "lbfi9hhe1i06wly52k8996i9s"
client_id = '5c3b13a967bc4bf598898a7eaac6e54a'
redirect_uri = 'spotify-app-ec://callback'
client_secret = 'de48c9b902314b31a712e838ffe43fa1'

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == "GET":
        return "finished"
        # user_id = 'lbfi9hhe1i06wly52k8996i9s'
        # authToken ="BQBwAtNXf4-pEa_KZbf7Jt9fscJu02JtJaJ5P9t4ditQ8XsXImw9zcRC_RUSlLxOEZKCvmo657A3Rk1DOjX-hBSqP93tpGRt6NbvwUryEtrZ3alOxujab51iTDsI3IAw-cy1ETdWFu4QfeFFPAxQrPCfCYORk614N28WILCEelDzFjORV-32zq8dGSpHK2yA6XiVDxU"

        # mind_aspect = "I"
        # energy_aspect = "N"
        # nature_aspect = "T"
        # tactics_aspect = "J"
        # identity_aspect = "T"
        # query = db.session.query(User).filter_by()
        # users = []
        # for user in query:
        #     users.append(user)
        # variables = users[0].keys()
        # df = pandas.DataFrame([[getattr(i,j) for j in variables] for i in users], columns = variables)
        # print(df)
        # return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/user/<user_id>", methods=["GET"])
def exists_in_db(user_id):
    users_in_db = db.session.query(User).filter_by(user_id=user_id)
    users = []
    for user in users_in_db:
        users.append(user)
    if len(users) == 0:
        return json.dumps({'exists':False}), 200, {'ContentType':'application/json'}
    return json.dumps({'exists':True}), 200, {'ContentType':'application/json'}

@app.route("/save-user", methods=["POST"])
def save_user():
    req_data = request.get_json(force=True) # force=True will make sure this works even if a client does not specify application/json
    
    print(req_data)
    user_id = req_data['userId']
    # mind_aspect = req_data['mindAspect']
    # tactics_aspect = req_data['tacticsAspect']
    # energy_aspect = req_data['energyAspect']
    # nature_aspect = req_data['natureAspect']
    # identity_aspect = req_data['identityAspect']
    # country = req_data['country']
    # user = User(user_id=user_id, mind_aspect=mind_aspect, tactics_aspect=tactics_aspect,
    #             energy_aspect=energy_aspect, nature_aspect=nature_aspect, identity_aspect=identity_aspect, country=country)
    # db.session.add(user)
    return user_id

@app.route("/save-playlists/<user_id>/<authToken>", methods=['GET'])
def save_playlist(user_id, authToken):
    for playlistId in get_playlists_by_user(user_id, authToken):
        save_tracks_by_playlist(user_id, playlistId, authToken)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/simple-recommend/<user_id>", methods=['GET'])
def simple_recommend(user_id):
    return recommend_by_popularity(user_id)

@app.route("/recommend/<user_id>", methods=['GET'])
def recommend(user_id):
    songs_by_users_query =db.session.query(SpotifyUserSongInPlaylist).filter_by(user_id=user_id)
    songs_by_users = []
    for song in songs_by_users_query:
        songs_by_users.append(song)

    if len(songs_by_users) > 10 :
        recommendations = db.session.query(Recommendation).filter_by(user_id=user_id, date_recommended_for=date.today()).all()
        recomm = []
        for rec in recommendations:
            recomm.append(rec.track_id)
        recomm1 = pd.DataFrame(recomm, columns=["track_id"])
        # print(recomm1["id"][0].user_id)
        # recomm1 = recomm1.drop(columns=['id', "user_id", "date_recommended_for"]).drop_duplicates(subset=['track_id'])
        return recomm1['track_id'].to_json()
    else:
        return recommend_by_popularity(user_id)

# @app.route("/run/recommend", methods=['GET'])
# def build_recommender_model():
#     from surprise import Reader, BaselineOnly, KNNBasic, Dataset, SVD
#     from surprise.model_selection import cross_validate
#     spotifyusers_songs_in_playlist = db.session.execute(    
#         "SELECT * FROM spotifyusersonginplaylist b FULL OUTER JOIN public.user v ON b.user_id = v.user_id")
#     spotifyusers_songs_in_playlist = pd.DataFrame(spotifyusers_songs_in_playlist, columns=["id", "user_id", "date_added", "track_id", "popularity", "explicit", "user_id2", "user_tb_id", "mind_aspect", "energy_aspect", "nature_aspect", "tactics_aspect", "identity_aspect", "country"])
#     spotifyusers_songs_in_playlist = spotifyusers_songs_in_playlist.drop(columns=['id', 'user_id2'])
#     spotifyusers_songs_in_playlist = spotifyusers_songs_in_playlist[
#         spotifyusers_songs_in_playlist['popularity'] > 80]
#     spotifyusers_songs_in_playlist['personality'] = spotifyusers_songs_in_playlist['mind_aspect'] + spotifyusers_songs_in_playlist['energy_aspect'] + \
#         spotifyusers_songs_in_playlist['nature_aspect'] + \
#         spotifyusers_songs_in_playlist['tactics_aspect']

#     songs = spotifyusers_songs_in_playlist['track_id'].reset_index()
#     songs = songs.drop(columns=['index'])
#     songs = songs.drop_duplicates(subset=['track_id']).reset_index()
#     songs = songs.rename(
#         columns={'track_id': 'spotify_track_id', 'index': 'track_id'})

#     spotifyusers_songs_in_playlist['listened'] = 1
#     spotifyusers_songs_in_playlist = spotifyusers_songs_in_playlist.drop(
#         columns=['mind_aspect', 'energy_aspect', 'nature_aspect', 'tactics_aspect', 'identity_aspect', 'date_added', 'explicit', 'popularity', 'user_tb_id'])
#     grouped = spotifyusers_songs_in_playlist
#     spotifyusers_songs_in_playlist['user_song'] = spotifyusers_songs_in_playlist['user_id'] + \
#         spotifyusers_songs_in_playlist['track_id']
#     grouped['user_song'] = grouped['user_id'] + grouped['track_id']
#     grouped = grouped.groupby(['user_song']).agg(
#         {'listened': 'count'}).reset_index()
#     grouped.rename(columns={'listened': 'score'}, inplace=True)
#     grouped = grouped.merge(spotifyusers_songs_in_playlist, on="user_song")
#     grouped = grouped.drop_duplicates(subset=['user_song'])
#     grouped = grouped.drop(columns=['country', 'listened', 'user_song'])
#     user_songs_ratings = grouped
#     del grouped

#     ratings_dict = {'itemID': list(user_songs_ratings.track_id),
#                     'userID': list(user_songs_ratings.user_id),
#                     'rating': list(user_songs_ratings.score)}
#     df = pd.DataFrame(ratings_dict)

#     reader = Reader(rating_scale=(0.5, 5.0))
#     data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
#     trainset = data.build_full_trainset()
#     algo = SVD()
#     algo.fit(trainset)
#     testset = trainset.build_anti_testset()
#     predictions = algo.test(testset)
#     top_n = get_top_n(predictions, n=10)
#     user_ids = []
#     for uid, user_ratings in top_n.items():
#         for user_rating in user_ratings:
#             recommendation = Recommendation(user_id=uid, track_id=user_rating[0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ])
#             db.session.add(recommendation)
#             db.session.commit()
#     user_ids = pd.DataFrame(user_ids, columns=['user_id', 'user_ratings'])
#     return user_ids.to_json()

def recommend_by_popularity(user_id):
    query = db.session.execute("SELECT * FROM public.spotifyusersonginplaylist")
    spotifyusers_songs_in_playlist = []
    for song in query:
        spotifyusers_songs_in_playlist.append(song)
    print(spotifyusers_songs_in_playlist)
    spotifyusers_songs_in_playlist = pd.DataFrame(spotifyusers_songs_in_playlist, columns=["id", "user_id", "date_added", "track_id", "popularity", "explicit"])
    pm = popularity_recommender_py()
    pm.create(spotifyusers_songs_in_playlist, 'user_id', 'track_id')
    recommended_songs = pm.recommend(user_id)
    print(recommended_songs)
    return recommended_songs['track_id'].to_json()


def set_user_personalities(user):
    mind_options = ["I", "E"]
    mind_weights = [47.95/100, 52.05/100]
    energy_options = ["S", "N"]
    energy_weights = [44.15/100, 55.85/100]
    nature_options = ["T", "F"]
    nature_weights = [45.33/100, 54.67/100]
    tactics_options = ["J", "P"]
    tactics_weights = [48.26/100, 51.74/100]
    identity_options = ["A", "T"]
    identity_weights = [49.5/100, 50.5/100]
    user.mind_aspect = numpy.random.choice(mind_options, p=mind_weights)
    user.energy_aspect = numpy.random.choice(energy_options, p=energy_weights)
    user.nature_aspect = numpy.random.choice(nature_options, p=nature_weights)
    user.tactics_aspect = numpy.random.choice(
        tactics_options, p=tactics_weights)
    user.identity_aspect = numpy.random.choice(
        identity_options, p=identity_weights)
    db.session.commit()


def get_playlists_by_user(user_id, authToken):
    spotify = spotipy.Spotify(auth=authToken)
    playlists = spotify.user_playlists(user_id)
    playlists_id = []
    offset_amount = math.ceil(playlists['total'] / playlists['limit'])
    for offset in numpy.arange(offset_amount):
        playlists1 = spotify.user_playlists(
            user_id, offset=offset*playlists['limit'])
        for playlist in playlists1['items']:
            playlists_id.append(playlist['id'])
    return playlists_id


def save_tracks_by_playlist(user_id, playlist_id, authToken):
    spotify = spotipy.Spotify(auth=authToken)
    tracks = spotify.user_playlist_tracks(user_id, playlist_id, offset=100)
    offset_amount = math.ceil(tracks['total'] / tracks['limit'])
    for offset in numpy.arange(offset_amount):
        tracks2 = spotify.user_playlist_tracks(
            user_id, playlist_id, offset=offset*tracks['limit'])
        for track in tracks2['items']:
            track_ = SpotifyUserSongInPlaylist(
                user_id, track['added_at'], track['track']['id'], track['track']['popularity'], track['track']['explicit'])
            db.session.add(track_)
            db.session.commit()


def get_all_playlsts(authToken):
    spotify = spotipy.Spotify(auth=authToken)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # countries = ['ec', 'fr','ar','fi','no','it','lt','ph','tw','nz','ee','tr','us','sv','cr','de','cl','jp','br','hn','gt','ch','hu','ca','pe','be','my','dk','bo','pl','at','pt','se','mx','pa','uy','is','es','cz','ie','nl','sk','co','sg','id','do','lu','gb','global','py','au','lv','gr','hk']
    countries = ['hn']
    mind_aspects = ['E', 'I']
    energy_aspects = ['S', 'N']
    nature_aspects = ['T', 'F']
    tactics_aspects = ['J', 'P']
    identity_aspects = ['A', 'T']
    for i in numpy.arange(len(countries)):
        try:
            print("Started with: " + countries[i])
            for letter in numpy.arange(len(letters)):
                pl = spotify.search(
                    letters[letter], type="playlist", market=countries[i], limit=50)
                offset_amount = math.ceil(
                    pl['playlists']['total'] / pl['playlists']['limit'])
                for offset in numpy.arange(offset_amount):
                    playlists = spotify.search(
                        q=letters[letter], type="playlist", market=countries[i], offset=offset+1178, limit=50)['playlists']['items']
                    print(str((offset*50)+1069)+"/"+str(offset_amount))
                    for playlist in playlists:
                        if playlist['owner']['id'] != 'spotify':
                            db.session.add(Playlist(
                                playlist_id=playlist['id'], name=playlist['name'], owner=playlist['owner']['id']))
                            db.session.add(
                                User(playlist['owner']['id'], "", "", "", "", "", country=countries[i]))
                            db.session.commit()

        except Exception as e:
            print(e)
        print("finished with country: " + countries[i-1])


def get_top_n(predictions, n=10):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

class popularity_recommender_py():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.popularity_recommendations = None
        
    #Create the popularity based recommender system model
    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

        #Get a count of user_ids for each unique song as recommendation score
        train_data_grouped = train_data.groupby([self.item_id]).agg({self.user_id: 'count'}).reset_index()
        train_data_grouped.rename(columns = {'user_id': 'score'},inplace=True)
    
        #Sort the songs based upon recommendation score
        train_data_sort = train_data_grouped.sort_values(['score', self.item_id], ascending = [0,1])
    
        #Generate a recommendation rank based upon score
        train_data_sort['Rank'] = train_data_sort['score'].rank(ascending=0, method='first')
        
        #Get the top 10 recommendations
        self.popularity_recommendations = train_data_sort.head(100)

    #Use the popularity based recommender system model to
    #make recommendations
    def recommend(self, user_id):    
        listened_songs = self.train_data[self.train_data['user_id']==user_id]['track_id']
        recommended_songs = self.popularity_recommendations
        recommended_songs['user_id'] = user_id
        #Bring user_id column to the front
        cols = recommended_songs.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        recommended_songs = recommended_songs[cols]
        
        for listened_song in listened_songs:
            recommended_songs = recommended_songs[recommended_songs['track_id']!=listened_song]
        
        recommended_songs = recommended_songs.head(10)
        
        return recommended_songs
    