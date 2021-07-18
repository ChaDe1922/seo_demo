#Import for data visualization
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Import API Requirements
import requests, os
import spotipy

#Import JSON
import json

#import SQL
import sqlalchemy
from sqlalchemy import create_engine


########################################################################
#                      FOR API INTERACTION                             #
########################################################################


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
       
       return auth_response, headers

#TEST 1: Is it receiving a list?
#TEST 2: Is the url valid
#TEST 3: Was each request successful
#TEST 4: Does each artist exist?
#TEST 5: Does it return a Pandas DataFrame
def pullDataFromAPIintoPandasDF(desArtistList, headers, filename):
       #Access endpoints base URL for spotify
       #do a GET request for each artist entered. Specify the url & the headers set for authentication. You can input parameters (params=) as to what limits you want on the json file that will be returned to you
       print("GETting request from Spofity API...")
       BASE_URL = 'https://api.spotify.com/v1/'
       
       rows = []
       id = 0
       
       for entry in desArtistList:
              print(entry, "request")
              
              r = requests.get(BASE_URL + 'search?q=' + entry + '&type=artist&limit=1', headers = headers)
              #print(artIdReq.status_code)
              d = r.json()
              
              artistInfo = d['artists']
              for item in artistInfo['items']:
                     artistName = item['name']
                     artistID = item['id']
                     print("Entry", id, "Artist ID for", artistName, ":", artistID)
                     
                     artistData = []
                     artistData.append(id)
                     artistData.append(item['name'])
                     artistData.append(item['id'])
                     artistData.append(item['genres'][0])
                     artistData.append(item['popularity'])
                     for key in item['followers']:
                            if key == 'total':
                                   artistData.append(item['followers'][key])
                     rows.append(artistData)
                     id += 1
                      
       #convert dictionary 'd' into pandas dataframe
       dataframe = pd.DataFrame(rows, columns=['id', 'Name','Artist ID', 'Genre', 'Popularity', 'Followers'])
       print("DataFrame Conversion Complete")
                     
       return dataframe

def loadNewData(desArtistList, headers, dataframe):
       #read the user artist requests
       for entry in desArtistList:
              print(entry, "request") 
              #Request info on those artists
              r = requests.get(BASE_URL + 'search?q=' + entry + '&type=artist&limit=1', headers = headers)
              d = r.json()
       
              #Parse their artist name and artist id from the requests
              artistInfo = d['artists']
              for item in artistInfo['items']:
                     artistName = item['name']
                     artistID = item['id']
       
       #Read the existing dataframe variables
       #Scan artistName and artistID columns in frame variable
       #if the dataframe variables match the parsed data from the response
       #print name already exists
       #do not append artist info to the dataframe
       #If the parsed and database variables do not match
       #print adding artistName
       #append artist data to dataframe
       #return the updated dataframe

########################################################################
#                      FOR USER INTERACTION                            #
########################################################################


#TEST 1: Is it receiving a dictionary?
#TEST 2: Is the user inputting strings?
#TEST 3: Is it returning a list?
def getArtistsRequest(headers):
       #Get artist names from user
       desArtistStr = (input("Enter up to 10 artists(Separated by commas): "))
       desArtistList = desArtistStr.split (", ")
       for i in range(len(desArtistList)):
              print("You entered:", i + 1, desArtistList[i])
              
       return desArtistList



########################################################################
#                           FOR DATA MIGRATION                         #
########################################################################


def saveSQLtoFile(filename, database_name):
       os.system('mysqldump -u root -pcodio ' + database_name + ' > ' + filename)
       
def loadSQLfromFile(filename, database_name):
       #create a database if it doesn't exist
       os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS ' + database_name + ' ;"')
       os.system("mysql -u root -pcodio "+ database_name + " > " + filename)

def createEngine(database_name):
       return  create_engine('mysql://root:codio@localhost/' + database_name '?charset=utf8', encoding='utf-8')

def updateDataset(database_name, table_name, filename):
       loadSQLfromFile(filename, database_name)
       df = pd.read_sql_table(table_name, con=createEngine(database_name))
       return loadNewData(desArtistList, df)

def saveDatasetToFile(database_name, table_name, filename, dataframe):
       print("Creating SQL from DataFrame...")
       dataframe.to_sql(table_name, con=createEngine(database_name), if_exists='replace', index=False,
                        dtype={'id' : sqlalchemy.types.INTEGER(),
                               'Name' : sqlalchemy.types.VARCHAR(length=255),
                               'Artist ID': sqlalchemy.types.VARCHAR(length=255),
                               'Genres': sqlalchemy.types.VARCHAR(length=255),
                               'Popularity' : sqlalchemy.types.INTEGER(),
                               'Followers' : sqlalchemy.types.INTEGER(),
                     })
       engine.execute('ALTER TABLE artists ADD PRIMARY KEY (`id`);')
       saveSQLtoFile(filename, database_name)
       
       
########################################################################
#                            MAIN DRIVER CODE                          #
########################################################################


def main():
       #Authentication variables
       CLIENT_ID = '744aee4ee39a4b6787e645452d1d36b4'
       CLIENT_SECRET = '7b72ec76041d4818b061e91ce613d780'
       AUTH_URL = 'https://accounts.spotify.com/api/token'
       
       #Environment Variables
       database_name = 'artist_collection'
       table_name = 'artists'
       filename = 'data-dump.sql'
       
       #FUNCTION CALLS
       auth_response, headers = requestAuth(CLIENT_ID, CLIENT_SECRET, AUTH_URL)
       print(type(headers))
       desArtistList = getArtistsRequest(headers)
       
       update_or_new = (input("Would you like to update the datebase or create a new one? (Enter 'update' or 'new')"))
       
       if update_or_new == 'update':
              df = updateDataset(database_name, table_name, filename)
              print(df)
              saveDatasetToFile(database_name, table_name, filename, df)
              print("Program Complete, Goodbye.")
       
       elif update_or_new == 'new':
              df = pullDataFromAPIintoPandasDF(desArtistList, headers, filename)
              print(df)
              saveDatasetToFile(database_name, table_name, filename, df)
              print("Program Complete, Goodbye.")
              
       else:
              print("You have entered an invalid value!")
       
       
       
       
       
if __name__ == "__main__":
       main()