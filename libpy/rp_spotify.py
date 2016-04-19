#Author: Rémi Pelletier
#File:   rp_spotify.py
#Desc.:  A module containing useful functions to gather music information using the Spotify web API.

#TODO: Add artist' genre and image url?
#TODO: Add album's genre?
#TODO: Change tracklist file name to 'Tracklist.txt' instead of '{ALBUM}.txt'?
#TODO: Change album cover file name to 'Cover.jpg' instead of '{ALBUM}.jpg'?

import sys
import os
import json
import urllib.request
import difflib

import rp_web
import rp_files
import rp_json


SPOTIFY_API_URL = 'https://api.spotify.com/v1'

SPOTIFY_SEARCH_TAG = '/search?&q='
SPOTIFY_TYPE_TAG = '&type='

SPOTIFY_TYPE_ARTIST = 'artist'
SPOTIFY_TYPE_ALBUM = 'album'
SPOTIFY_TYPE_TRACK = 'track'

JSON_TAG_ITEMS = 'items'
JSON_TAG_NAME = 'name'
JSON_TAG_ID = 'id'
JSON_TAG_URL = 'url'
JSON_TAG_TOTAL = 'total'
JSON_TAG_IMAGES = 'images'
JSON_TAG_ALBUM_TYPE = 'album_type'

ALBUM_TYPE_ALBUM = 'album'
ALBUM_TYPE_SINGLE  = 'single'
ALBUM_TYPE_COMPILATION = 'compilation'

ALBUM_COVER_EXT = '.jpg'
MUSIC_INFO_EXT = '.txt'

NO_RESULTS_ERROR_MESSAGE = 'There were no results found for this search request.'


class Artist:
    name = ''
    id = ''
    albums = []

    def __init__(self, artist_name, artist_id, albums_list):
        self.name = artist_name
        self.id = artist_id
        self.albums = albums_list


class Album:
    name = ''
    id = ''
    album_type = ''
    cover_url = ''
    tracks = []

    def __init__(self, album_name, album_id, album_type_str, album_cover_url, album_tracks):
        self.name = album_name
        self.id = album_id
        self.album_type = album_type_str
        self.cover_url = album_cover_url
        self.tracks = album_tracks


class Track:
    name = ''
    id = ''
    def __init__(self, track_name, track_id):
        self.name = track_name
        self.id = track_id


class NoResultsException(Exception):
    pass



#-------------------------------------Conversions----------------------------------------

#Converts a string identifying the type of an element to it's URL tag counterpart.
def typeToUrlTag(type):
    return '/' + type + 's/'

#Converts a string identifying the type of an element to it's JSON tag counterpart.
def typeToJsonTag(type):
    return type + 's'

#----------------------------------------------------------------------------------------



#--------------------------------------Search URL----------------------------------------

#Creates the Spotify API call URL for the given search request and search type.
def getSpotifySearchUrl(search_request, search_type):
    return SPOTIFY_API_URL + SPOTIFY_SEARCH_TAG + rp_files.removeAccents(search_request.replace(' ', '+')) + SPOTIFY_TYPE_TAG + search_type

#Creates the Spotify API call URL for the given artist search request.
def getArtistSearchUrl(search_request):
    return getSpotifySearchUrl(search_request, SPOTIFY_TYPE_ARTIST)

#Creates the Spotify API call URL for the given album search request.
def getAlbumSearchUrl(search_request):
    return getSpotifySearchUrl(search_request, SPOTIFY_TYPE_ALBUM)

#Creates the Spotify API call URL for the given track search request.
def getTrackSearchUrl(search_request):
    return getSpotifySearchUrl(search_request, SPOTIFY_TYPE_TRACK)

#----------------------------------------------------------------------------------------



#----------------------------------------ID URL------------------------------------------

#Creates the Spotify API call URL using the given type and ID.
def getSpotifyIdUrl(element_type, element_id):
    return SPOTIFY_API_URL + typeToUrlTag(element_type) + element_id

#Creates the artist's page URL using the artist's ID. 
def getArtistUrl(artist_id):
    return getSpotifyIdUrl(SPOTIFY_TYPE_ARTIST, artist_id)

#Creates the album's page URL using the album's ID. 
def getAlbumUrl(album_id):
    return getSpotifyIdUrl(SPOTIFY_TYPE_ARTIST, album_id)

#Creates the track's page URL using the track's ID.
def getTrackUrl(track_id):
    return getSpotifyIdUrl(SPOTIFY_TYPE_ARTIST, track_id)

#Creates the artist's albums' page URL using the artist's ID. 
def getArtistAlbumsUrl(artist_id):
    return getSpotifyIdUrl(SPOTIFY_TYPE_ARTIST, artist_id) + typeToUrlTag(SPOTIFY_TYPE_ALBUM)

#Creates the album's tacklist's page URL using the album's ID. 
def getAlbumTracksUrl(album_id):
    return  getSpotifyIdUrl(SPOTIFY_TYPE_ALBUM, album_id) + typeToUrlTag(SPOTIFY_TYPE_TRACK)

#----------------------------------------------------------------------------------------



#-----------------------------------Find ID and Name-------------------------------------

#Finds the name and id of an element using a given search request (if no result is found, the NoResultsException is raised).
def findElement(search_request, search_type):
    json_dict = rp_json.getJsonDictionnary(getSpotifySearchUrl(search_request, search_type))[typeToJsonTag(search_type)]
    if(json_dict[JSON_TAG_TOTAL] == 0):
        raise NoResultsException(NO_RESULTS_ERROR_MESSAGE)
    elements_list = json_dict[JSON_TAG_ITEMS]
    best_match = difflib.get_close_matches(search_request.lower(), [elm[JSON_TAG_NAME] for elm in elements_list[:5]], 1)
    element = elements_list[0] if len(best_match) == 0 else next(e for e in elements_list[:5] if e[JSON_TAG_NAME] == best_match[0])
    return element[JSON_TAG_NAME], element[JSON_TAG_ID]

#Finds the name and id of an artist using a given search request (if no result is found, the NoResultsException is raised).
def findArtist(search_request):
    return findElement(search_request, SPOTIFY_TYPE_ARTIST)

#Finds the name and id of an album using a given search request (if no result is found, the NoResultsException is raised).
def findAlbum(search_request):
    return findElement(search_request, SPOTIFY_TYPE_ALBUM)

#Finds the name and id of a track using a given search request (if no result is found, the NoResultsException is raised).
def findTrack(search_request):
    return findElement(search_request, SPOTIFY_TYPE_TRACK)

#----------------------------------------------------------------------------------------



#-------------------------------JSON to Spotify instance---------------------------------

#Creates an instance of Artist from a JSON dictionnary.
def getArtistFromJson(artist_dict):
    return Artist(artist_dict[JSON_TAG_NAME], artist_dict[JSON_TAG_ID], getArtistAlbums(artist_dict[JSON_TAG_ID]))

#Creates an instance of Album from a JSON dictionnary.
def getAlbumFromJson(album_dict):
    return Album(album_dict[JSON_TAG_NAME], album_dict[JSON_TAG_ID], album_dict[JSON_TAG_ALBUM_TYPE], album_dict[JSON_TAG_IMAGES][0][JSON_TAG_URL], getAlbumTracks(album_dict[JSON_TAG_ID]))

#Creates an instance of Track from a JSON dictionnary.
def getTrackFromJson(track_dict):
    return Track(track_dict[JSON_TAG_NAME], track_dict[JSON_TAG_ID])

#Creates an instance of Artist using the JSON dictionnary obtained by querying the given id.
def getArtistById(artist_id):
    artist_dict = rp_json.getJsonDictionnary(getArtistUrl(artist_id))
    return getArtistFromJson(artist_dict)

#Creates an instance of Artist using the JSON dictionnary obtained by querying the given id.
def getAlbumById(album_id):
    album_dict = rp_json.getJsonDictionnary(getAlbumUrl(album_id))
    return getAlbumFromJson(album_dict)

#Creates an instance of Artist using the JSON dictionnary obtained by querying the given id.
def getTrackById(track_id):
    track_dict = rp_json.getJsonDictionnary(getTrackUrl(track_id))
    return getTrackFromJson(track_dict)

#Creates a list of Albums of an artist given by his ID.
def getArtistAlbums(artist_id, only_albums = True):
    albums_list = rp_json.getJsonItems(getArtistAlbumsUrl(artist_id))
    albums = []
    for entry in albums_list:
        if (not only_albums or entry[JSON_TAG_ALBUM_TYPE] == ALBUM_TYPE_ALBUM) and not any(album.name == entry[JSON_TAG_NAME] for album in albums):
            albums.append(getAlbumFromJson(entry))
    return albums

#Creates a list of Tracks of an album given by it's ID.
def getAlbumTracks(album_id):
    tracks_list = rp_json.getJsonItems(getAlbumTracksUrl(album_id))
    tracks = []
    for entry in tracks_list:
        if not any(track.name == entry[JSON_TAG_NAME] for track in tracks):
            tracks.append(getTrackFromJson(entry))       
    return tracks

#----------------------------------------------------------------------------------------



#--------------------------------------Formatting----------------------------------------

#Removes special versions of already existing albums in a list of albums and returns the new list.
def removeMultipleAlbumVersions(albums):
    albums.sort(key = lambda album: len(album.name))
    clean_list = []
    for album in albums:
        if not any((not album2.name == album.name and album2.name in album.name) for album2 in albums):
            clean_list.append(album)
    return clean_list

#Removes the singles from an album list and returns the new list.
def removeSingles(albums):
    return [].append(album for album in albums if not album.album_type == ALBUM_TYPE_SINGLE)

#Removes the compilations from an album list and returns the new list.
def removeCompilations(albums):
    return [].append(album for album in albums if not album.album_type == ALBUM_TYPE_COMPILATION)

#----------------------------------------------------------------------------------------



#--------------------------------------Save data-----------------------------------------

#Downloads the demanded album cover and saves it to the given directory.
def saveAlbumCover(album, dir = ''):
    rp_web.downloadFile(album.cover_url, os.path.join(dir, rp_files.cleanFileName(album.name) + ALBUM_COVER_EXT))


#Saves the tracklist of a given album to the specified direcotry.
def saveTracklist(album, dir=''):
    clean_album_name = rp_files.cleanFileName(album.name)
    tracklist_path = os.path.join(dir, clean_album_name + MUSIC_INFO_EXT)
    if not os.path.exists(tracklist_path):
        with open(tracklist_path, 'w') as file:
            for track in album.tracks:
                file.write(track.name + '\n')
            file.write('\n')


#Saves the discography of a given artist to the specified directory.
def saveDiscography(artist, dir=''):
    clean_artist_name = rp_files.cleanFileName(artist.name)
    discography_path = os.path.join(dir, clean_artist_name + MUSIC_INFO_EXT)
    if not os.path.exists(discography_path):
        with open(discography_path, 'w') as file:
            file.write('-'*30 + artist.name + '-'*30)
            for album in artist.albums:
                file.write('\n\n\n' + '-'*10 + album.name + '-'*10)
                for track in album.tracks:
                    file.write('\n' + track.name)

#----------------------------------------------------------------------------------------
