# Song_Recommendation
#Sem1 Mini Project


import spotipy
import numpy as np
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials


#Authorization for Spotify API
cid= '94a98c9f1fb549f8bbb375fde0e347be'
secret= '1f245c1e6a65416684928f7bffbdfff0'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)



#Getting Playlist and Song info
def call_playlist(creator, playlist_id):
    
    #step 1: Create Dataframe

    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    #step 2: 
    
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:
        # Create Empty Dictionary
        playlist_features = {}
        # To get corresponding Values
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        
        # To get Audio Features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]
        
        # Merge into final Dataframe
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)

    #Step 3: Return Dataframe
        
    return playlist_df

playlist_link= input("Enter Playlist Link: ")
playlist_id=playlist_link[34:56]
print(playlist_id)

a= call_playlist("spotify",playlist_id)

#Copying DataFrame to Excel
a.to_excel("C:/Users/bhave/OneDrive/Desktop/spot project/Playlist_Info.xlsx") #use different path/directory according to your computer
