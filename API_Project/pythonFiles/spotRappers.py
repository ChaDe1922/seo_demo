#Import for data visualization
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Import API Requirements
import requests
import spotipy

#Import JSON
import json

#import SQL
import sqlalchemy
from sqlalchemy import create_engine

#Authentication variables
CLIENT_ID = '744aee4ee39a4b6787e645452d1d36b4'
CLIENT_SECRET = '7b72ec76041d4818b061e91ce613d780'

#Authenticate myself with a post request including the url and my creds
AUTH_URL = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

#Print the response to my request
print(auth_response.status_code)

#convert the response, "auth_response" to json using .json()
auth_response_data = auth_response.json()

#pull the access token from the response and save it in a variable "access_token"
access_token = auth_response_data['access_token']

#save the token to the API to use in my GET request headers
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

#Access endpoints base URL for spotify
BASE_URL = 'https://api.spotify.com/v1/'

#Variables for artist data I want to collect, artist-ids
lil_baby = '5f7VJjfbwm532GiveGC0ZK'
drake = '3TVXtAsR1Inumwj472S9r4'
lil_uzi_vert = '4O15NlyKLIASxsJ0PrXPfz'

#do a GET request. Specify the url & the headers set for authentication
#you can input parameters (params=) as to what limits you want on the json file that will be returned to you
r = requests.get(BASE_URL + 'artists?ids=' + lil_baby + "," + drake + "," + lil_uzi_vert, headers = headers)

#convert whatever is returned into JSON
d = r.json()


#convert dictionary 'd' into pandas dataframe
rows=[]
for artist in d['artists']:
    artistData = []
    artistData.append(artist['name'])
    artistData.append(artist['genres'][0:2])
    artistData.append(artist['popularity'])
    for key in artist['followers']:
        if key == 'total':
            artistData.append(artist['followers'][key])
    rows.append(artistData)
    
pd.DataFrame(rows, columns=['Name', 'Genres', 'Popularity', 'Followers']).head()

#create engine object
engine = create_engine('mysql://root:codio@localhost/rappers')
