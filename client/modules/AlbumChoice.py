import csv
import random
import re
import os

WORDS = ["Album","Play","Music"]

def get_catalogue():
        fn = os.path.join(os.path.dirname(__file__), 'Catalogue.csv')
        csv_file = open(fn, "rt") 
        return(csv.reader(csv_file))


def get_random_album_from_decade(decade):
        decade_albums = []
        for album in get_catalogue():
                if album[3] == decade:
                        decade_albums.append(album)

        try:
                return random.choice(decade_albums)
        except:
                return None

def get_random_album_from_genre(genre):
        genre_albums = []
        for album in get_catalogue():
                if album[2] == genre:
                        genre_albums.append(album)

        try:
                return random.choice(genre_albums)
        except:
                return None

def get_random_album_from_all():
        try:
                albums = list(get_catalogue())
                return random.choice(albums)
        except:
                return None


def filter(text):
        #Checks if Genre, year or all mentioned. Returns False if not true, album list otherwise.
        decades = ["60s", "70s", "80s", "90s", "2000s", "2010s"]
        decade_trans = {"60s":"1960s", "70s":"1970s", "80s":"1980s", "90s":"1980s", "2000s":"2000s", "2010s":"2010s"}
        
        genres = ["Pop", "Rock", "Punk"]

        if bool(re.search('All', text, re.IGNORECASE)):
                album = get_random_album_from_all()
                return album

        for genre in genres:
                if bool(re.search(genre, text, re.IGNORECASE)):
                        album = get_random_album_from_genre(genre)
                        return album

        for decade in decades:
                if bool(re.search(decade, text, re.IGNORECASE)):
                        album = get_random_album_from_decade(decade_trans[decade])
                        return album
        return False

def say_album(album, mic):
        '''Album: [ARTIST,ALBUM_TITLE,GENRE,DECADE]'''
        openers = ["I think you should listen to ", "Why dont you try ", "I suggest ", ""]
        closers = [". You'll love it.", ".", ", it's great!", ". It's one of my favourites."]

        mic.say(random.choice(openers) + album[1] + " by " + album[0] + random.choice(closers))

        return

def isValid(text):
	return bool(re.search(r'\bAlbum\b', text, re.IGNORECASE))

def handle(text, mic, profile):
        #Filters original query for album, otherwise asks for specifics
        album = filter(text)
        if not album:                       
                mic.say("What genre or decade do you want me to choose from?")
                response = mic.activeListen()
                album = filter(response)
                if not album:
                        mic.say("I'm sorry, Toby I'm afraid I can't do that.")
                        return False

        try:
                say_album(album, mic)
        except Exception as e:
                print e
                mic.say("I'm sorry, I had an error with that album. Please try again.")
