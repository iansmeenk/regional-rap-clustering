import spotipy
import spotipy.util as util
from pandas import DataFrame, Series
import pandas as pd
from SpotipyCredentials import *
from SpotipyWrapperFunctions import *

scope = 'user-library-read'

token = util.prompt_for_user_token(username,scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)
if token:
	sp = spotipy.Spotify(auth=token)
	df = DataFrame()

 
	playlist_ids = {'Boom Bap': '6dkS1ujMA6PekEjyEfychz', 
					'G-Funk': '7zL8KplynmmUfNfim5miw5', 
					'Trap': '4ZI8bMpRNnU67DYNSczhUv'}
	for genre in playlist_ids.keys():
		genre_df = CreatePlaylistDF(playlist_ids[genre], spotipy_client=sp, username=username)
		genre_df_full = AddAudioFeatures(genre_df, spotipy_client=sp)
		genre_df_full['genre'] = genre
		df = df.append(genre_df_full)

	df.to_csv('data/playlists1.csv', index=False)
