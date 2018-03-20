import pandas as pd
import spotipy
from pandas import DataFrame
from math import ceil


def CreatePlaylistDF(playlist_id, spotipy_client, username):
    playlist_dict = spotipy_client.user_playlist_tracks(user=username, playlist_id=playlist_id)
    playlist_dict_list = playlist_dict['items']
    playlist_rows = []
    for song in playlist_dict_list:
        row = {}
        row['id'] = song['track']['id']
        row['title'] = song['track']['name']
        row['artistPrimary'] = song['track']['artists'][0]['name']
        row['artists'] = ', '.join([song['track']['artists'][i]['name'] for i in range(len(song['track']['artists']))])
        row['album'] = song['track']['album']['name']
        row['year'] = song['track']['album']['release_date'][:4]
        row['songLength'] = song['track']['duration_ms']
        playlist_rows.append(row)

    return DataFrame(playlist_rows)

def AddAudioFeatures(df_with_ids, spotipy_client):
    ids = list(df_with_ids['id'])
    bin_n = ceil(len(ids) / 50)
    ids_chunked = [ids[(i*50):(50*(i+1))] for i in range(bin_n)]
    
    for i in range(len(ids_chunked)):
        if i == 0:
            df = DataFrame(spotipy_client.audio_features(ids_chunked[i]))
        else:
            df = df.append(DataFrame(spotipy_client.audio_features(ids_chunked[i])))
    df_full = pd.merge(df_with_ids, df, on='id')
    return df_full