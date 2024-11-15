#Importing required Libraries
import spotipy
import numpy as np
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import PySimpleGUI as sg




#Authorization for Spotify API
cid= ''
secret= ''

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)



def step1_Info():
    #Getting Playlist and Song info
    def call_playlist(creator, playlist_id):
        
        #step 1: Create Dataframe

        playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
        
        playlist_df = pd.DataFrame(columns = playlist_features_list)
        
        #step 2: Fetching Song Details
        
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


    playlist_link= link
    playlist_id=playlist_link[34:56] #Gets Playlist ID from the entered link
    #print("Play list ID: ", playlist_id)

    global input_playlist
    input_playlist = call_playlist("spotify",playlist_id)


    #Copying DataFrame to Excel
    input_playlist.to_excel("C:/Users/bhave/OneDrive/Desktop/spot project/Playlist_Info.xlsx") #use different path/directory according to your computer
    #print("Excel Document Created!")




database=pd.DataFrame()     #Creating an empty dataframe to copy values from pre-existing excel sheet
database = pd.read_excel(r'C:/Users/bhave/OneDrive/Desktop/spot project/English.xlsx')

database1 = pd.read_excel(r'C:/Users/bhave/OneDrive/Desktop/spot project/Playlist_Info.xlsx')       #same as 'input_playlist' from 'step1_Info'

final_database = pd.concat([database,database1], ignore_index=True)     #merging both dataframes in another dataframe so that you can use this as a reference database to select the recommended songs from





def step2_algorithm():
    #Start of algorithm
    def_column_headers = final_database.loc[:,["danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]]
    column_headers=def_column_headers.to_numpy()


    scaler = MinMaxScaler()
    normalized_a =scaler.fit_transform(column_headers)


    # Create a pandas series with song titles as indices and indices as series values 
    indices = pd.Series(database1.index, index=database1['track_name']).drop_duplicates()

    # Create cosine similarity matrix based on given matrix
    cosine = cosine_similarity(normalized_a)

    def generate_recommendation(song_title, model_type=cosine ):
        
        #Purpose: Function for song recommendations 
        #Inputs: song title and type of similarity model
        #Output: Pandas series of recommended songs
        
        # Get song indices
        index=indices[song_title]

        # Get list of songs for given songs
        score=list(enumerate(model_type[indices[song_title]]))

        # Sort the most similar songs
        similarity_score = sorted(score,key = lambda x:x[1],reverse = True)

        # Select the top-10 recommend songs
                                        #Number of songs
        similarity_score = similarity_score[1:2]
        top_songs_index = [i[0] for i in similarity_score]

        # Top 10 recommende songs
        top_songs=final_database['track_name'].iloc[top_songs_index]

        return top_songs


    #print("Recommended Songs:")




    #All song Names in the playlist
    for (columnName, columnData) in database1.items():
        if columnName=='artist' or columnName=='album':
            continue
        if columnName=='track_id':
            break
        song_names=columnData.values

    #Each Song name from above gets 1 song recommended
    recommend_list=list()
    for i in song_names:
        a=((generate_recommendation(i,cosine).values))
        recommend_list.append(a)




    #Putting the songs in a 'set' to prevent repeated songs
    global top_recommend
    top_recommend=set()
    for i in recommend_list:
        m=str(i)
        o=m[2:-2]
        top_recommend.add(o)

    #print(top_recommend)


    recommend_index=list()
    temp=list()
    for i in range(0,len(final_database.index)):
        if final_database.iloc[i]['track_name'] in temp:
            continue
        elif final_database.iloc[i]['track_name'] in top_recommend:
            temp.append(final_database.iloc[i]['track_name'])
            #print(i,final_database.iloc[i]['track_name'])
            recommend_index.append(i)

    #print(recommend_index) #index of recommended songs which is used to get 'track id' which is required to make the website link




global link
layout = [
    [sg.Image(filename="C:/Users/bhave/OneDrive/Desktop/spot project/download.png")],
    [sg.Text('Enter Playlist Link:')],
    [sg.InputText()],
    [sg.Button('Submit')]
]

window = sg.Window('Text Input', layout)
event, values = window.Read()

if event == 'Submit':
    link = values[1]

window.Close()



step1_Info()
step2_algorithm()



value = list(top_recommend)
temp=list()
for i in value:
    a=list()
    a.append(i)
    temp.append(a)
    #print(temp)



layout = [
        [sg.Table(values = temp, headings=["Song Name"],key='-TABLE-',justification='left')]
    ]
window = sg.Window("Database", layout)

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "button":
        window.close()




