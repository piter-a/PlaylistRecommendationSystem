import spotipy
import Credentials
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth

scopes = ["user-follow-read", 'ugc-image-upload', 'user-read-playback-state',
          'user-modify-playback-state', 'user-read-currently-playing', 'user-read-private',
          'user-read-email', 'user-follow-modify', 'user-follow-read', 'user-library-modify',
          'user-library-read', 'streaming', 'app-remote-control', 'user-read-playback-position',
          'user-top-read', 'user-read-recently-played', 'playlist-modify-private', 'playlist-read-collaborative',
          'playlist-read-private', 'playlist-modify-public']

auth_manager = SpotifyOAuth(
    client_id=Credentials.cid, client_secret=Credentials.secret, redirect_uri=Credentials.redirect_uri, scope=scopes
)

sp = spotipy.Spotify(auth_manager=auth_manager)

curr_user = sp.current_user()
user_id = curr_user['id']

def getTopArtists(number_of_artists, timespan):

    top_artists = sp.current_user_top_artists(limit = number_of_artists, time_range = timespan)
    top_artists_info = []

    for i in range(len(top_artists['items'])):
        artist = top_artists['items'][i]['name']
        followers = top_artists['items'][i]['followers']['total']
        genres = top_artists['items'][i]['genres']
        artist_id = top_artists['items'][i]['id']
        top_artists_info.append([
            artist, followers, genres, artist_id
        ])

    return top_artists_info

def getTopTracks(number_of_tracks, timespan):

    top_tracks = sp.current_user_top_tracks(limit = number_of_tracks, time_range = timespan)
    top_tracks_info = []

    for i in range(len(top_tracks['items'])):
        artist = top_tracks['items'][i]['artists'][0]['name']
        song = top_tracks['items'][i]['name']
        album = top_tracks['items'][i]['album']['name']
        song_id = top_tracks['items'][i]['id']
        top_tracks_info.append([
            artist, song, album, song_id
        ])

    return top_tracks_info

def getRecentlyPlayed(number_of_tracks):

    recent_tracks = sp.current_user_recently_played(limit = number_of_tracks)
    recent_tracks_info = []

    for i in range(len(recent_tracks['items'])):
        artist = recent_tracks['items'][i]['track']['artists'][0]['name']
        song = recent_tracks['items'][i]['track']['name']
        album = recent_tracks['items'][i]['track']['album']['name']
        song_id = recent_tracks['items'][i]['track']['id']
        recent_tracks_info.append([
            artist, song, album, song_id
        ])

    return recent_tracks_info

def getIds(seed):

    seed_ids = []

    for i in range(len(seed)):
        seed_id = seed[i][3]
        seed_ids.append(seed_id)

    return seed_ids

def getArtistBasedRecommendations(artist_ids, number_of_recs):

    recs = sp.recommendations(seed_artists = artist_ids, limit = number_of_recs)
    rec_ids = []

    for i in range(len(recs['tracks'])):
        song_id = recs['tracks'][i]['id']
        rec_ids.append(song_id)

    return rec_ids

def getSongBasedRecs(song_ids, number_of_recs):

    recs = sp.recommendations(seed_tracks = song_ids, limit = number_of_recs)
    rec_ids = []

    for i in range(len(recs['tracks'])):
        song_id = recs['tracks'][i]['id']
        rec_ids.append(song_id)

    return rec_ids

def createPlaylist(user_id, playlist_name):
    
    playlist = sp.user_playlist_create(user = user_id, name = playlist_name)

    return playlist['id']

def populatePlaylist(user_id, pl_id, songs):

    sp.user_playlist_add_tracks(user = user_id, playlist_id = pl_id, tracks = songs)


print('Welcome to playlist recommendation system\n')

songs_or_artists = input('Would you like to make a playlist based on your top songs or artists?\n')

no_of_items = input('How many entries would you like to visualize? (Max 50)\n')

if (songs_or_artists == 'songs'):

    timespan = input('Select the time range(short, medium, long, or recent): \n')

    if (timespan == 'short'):
        top_tracks = getTopTracks(number_of_tracks = no_of_items, timespan = 'short_term')

    elif (timespan == 'medium'):
        top_tracks = getTopTracks(number_of_tracks = no_of_items, timespan = 'medium_term')

    elif (timespan == 'long'):
        top_tracks = getTopTracks(number_of_tracks = no_of_items, timespan = 'long_term')
    
    else:
        top_tracks = getRecentlyPlayed(number_of_tracks = no_of_items)

    print('Here are your favourite tracks in selected time range:\n')

    for i in range(len(top_tracks)):
        print(f'{i + 1}.{top_tracks[i][0]} - {top_tracks[i][1]}\n')

    track_selection = input('Choose numbers of up to 5 songs based on which to create your new playlist. Use song numbers separated by a space\n')
    track_selection = track_selection.split()

    seed_songs = [top_tracks[int(track) - 1] for track in track_selection]
    song_ids = getIds(seed = seed_songs)

    playlist_name = input('What would you like to name your playlist?\n')
    playlist = createPlaylist(user_id = user_id, playlist_name = playlist_name)

    number_of_songs = input('How many songs your new playlist contain?(max 100)\n')

    recs = getSongBasedRecs(song_ids = song_ids, number_of_recs = int(number_of_songs))

    populatePlaylist(user_id = user_id, pl_id = playlist, songs = recs)

    print('Your playlist has been created and added to your spotify account. Enjoy! :)')

elif (songs_or_artists == 'artists'):
    timespan = input('Select the time range(short, medium, or long): \n')

    if (timespan == 'short'):
        top_artists = getTopArtists(number_of_artists = no_of_items, timespan = 'short_term')

    elif (timespan == 'medium'):
        top_artists = getTopArtists(number_of_artists = no_of_items, timespan = 'medium_term')

    elif (timespan == 'long'):
        top_artists = getTopArtists(number_of_artists = no_of_items, timespan = 'long_term')
    
    print('Here are your favourite artists in selected time range:\n')

    for i in range(len(top_artists)):
        print(f'{i + 1}.{top_artists[i][0]}\n')

    artist_selection = input('Choose numbers of up to 5 artists based on which to create your new playlist. Use artist numbers separated by a space\n')
    artist_selection = artist_selection.split()

    seed_artists = [top_artists[int(artist) - 1] for artist in artist_selection]
    artist_ids = getIds(seed = seed_artists)

    playlist_name = input('What would you like to name your playlist?\n')
    playlist = createPlaylist(user_id = user_id, playlist_name = playlist_name)

    number_of_songs = input('How many songs your new playlist contain?(max 100)\n')

    recs = getSongBasedRecs(song_ids = artist_ids, number_of_recs = int(number_of_songs))

    populatePlaylist(user_id = user_id, pl_id = playlist, songs = recs)

    print('Your playlist has been created and added to your spotify account. Enjoy! :)') 