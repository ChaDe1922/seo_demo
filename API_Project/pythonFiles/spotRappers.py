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
AUTH_URL = 'https://accounts.spotify.com/api/token'

#TEST 1: Check for a CLIENT_ID, CLIENT_SECRET, and AUTH_URL
#TEST 2: Check if inputs are strings
#TEST 3: Check for presence of response code
#TEST 4: Check for successful response code
#Test 5: Is there an access_token?
#Test 6: Does it return something?
#Test 7: Does it return a dictionary
def requestAuth(CLIENT_ID, CLIENT_SECRET, AUTH_URL):
       #Authenticate myself with a post request including the url and my creds
       print("Requesting Authentication...")
       auth_response = requests.post(AUTH_URL, {
       'grant_type': 'client_credentials',
       'client_id': CLIENT_ID,
       'client_secret': CLIENT_SECRET,
       })

       #check for proper response code
       if auth_response.status_code == 200:
              #Print the response to my request
              print(auth_response.status_code, "Authentication Successful\n")
       else:
              print(auth_response.status_code, "There was some type of error!\n")
              
       #convert the response to JSON, pull the access token, and save the token to the API to use in my GET request headers
       auth_response_data = auth_response.json()
       access_token = auth_response_data['access_token']
       
       #Set Authorization headers
       headers = {
              'Authorization': 'Bearer {token}'.format(token=access_token)
       }
       
       return headers




#TEST 1: Is it receiving a dictionary?
#TEST 2: Is the user inputting strings?TEST
#TEST 3: Is it returning a list?
def getArtistsRequest(headers):
       #Get artist names from user
       desArtistStr = (input("Enter up to 10 artists(Separated by commas): "))
       desArtistList = desArtistStr.split (", ")
       for i in range(len(desArtistList)):
              print("You entered:", i + 1, desArtistList[i])
              
       return desArtistList

#TEST 1: Is it receiving a list?
#TEST 2: Is the url valid
#TEST 3: Was each request successful
#TEST 4: Does each artist exist?
#TEST 5: Does it return a Pandas DataFrame
def getArtistData(desArtistList):
       #Access endpoints base URL for spotify
       #do a GET request for each artist entered. Specify the url & the headers set for authentication. You can input parameters (params=) as to what limits you want on the json file that will be returned to you
       print("GETting request from Spofity API...")
       BASE_URL = 'https://api.spotify.com/v1/'
       
       rows = []
       
       for entry in desArtistList:
              print(entry, "request")
              r = requests.get(BASE_URL + 'search?q=' + entry + '&type=artist&limit=1', headers = headers)
              #print(artIdReq.status_code)
              d = r.json()
              
              artistInfo = d['artists']
              for item in artistInfo['items']:
                     artistName = item['name']
                     artistID = item['id']
                     print("Artist ID for", artistName, ":", artistID)
                     
                     artistData = []
                     artistData.append(item['name'])
                     artistData.append(item['id'])
                     artistData.append(item['genres'][0])
                     artistData.append(item['popularity'])
                     for key in item['followers']:
                            if key == 'total':
                                   artistData.append(item['followers'][key])
                     rows.append(artistData)

                                   
       #convert dictionary 'd' into pandas dataframe
       artistDF = pd.DataFrame(rows, columns=['Name','Artist ID', 'Genre', 'Popularity', 'Followers'])
       print("DataFrame Conversion Complete")
                     
       return artistDF

#TEST 1: Does it accept a dataframe & reject all others
#TEST 2: Does each header exist
#TEST 3: Does the successMessage return
def sendToSQL(artistDF):
       #create engine object
       engine = create_engine('mysql://root:codio@localhost/artists')

       #create and send sql table from my dataframe
       print("Creating SQL from DataFrame...")
       artistDF.to_sql('artists', con=engine, if_exists='replace', index=False,
                     dtype={'Name' : sqlalchemy.types.VARCHAR(length=255),
                            'Artist ID': sqlalchemy.types.VARCHAR(length=255),
                            'Genres': sqlalchemy.types.VARCHAR(length=255),
                            'Popularity' : sqlalchemy.types.INTEGER(),
                            'Followers' : sqlalchemy.types.INTEGER(),
                      
                     })

       successMessage = print("SQL Table Sent Successfully!")
       
       return successMessage
       

#FUNCTION CALLS
headers = requestAuth(CLIENT_ID, CLIENT_SECRET, AUTH_URL)
#print(type(headers))
desArtistList = getArtistsRequest(headers)
artistDF = getArtistData(desArtistList)
print(artistDF)

successMessage = sendToSQL(artistDF)
print(successMessage)
print("Program Complete, Goodbye.")