################################################################################
# To DO
# Sporify Contorl
# Update timetable
# Search Internet
# Set up lesenters to control things like when i get an email or ext
################################################################################

#Imports
import os
import ssl
from os import system
import webbrowser
from webbrowser import open_new_tab
import osascript
import pyttsx3
import datetime
from datetime import date
from subprocess import call
import json
from pyowm import OWM
from pyowm.utils import timestamps
import wolframalpha as wolframalpha
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
from Spotify.Spotify_Backend import *
#import FaceRecog as fr //WIP//
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

engine = pyttsx3.init()

#WishMe Function. Just to say Good morning or Good evening depending on time of day.
def wishme():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour<12:
        greeting = "Good Morning"
    elif hour >=12 and hour < 18:
        greeting = "Good Afternoon"
    elif hour >=18 and hour < 24:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"

    greeting = "{} Sir".format(greeting)
    return (greeting)


#Get Time and Date functions and returns the values
def gettime(inp):
    now = datetime.datetime.now()
    time = now.strftime("%H:%M")
    return ("the time is {}".format(time))

def getdate(inp):
    y = int(datetime.datetime.now().year)
    m = int(datetime.datetime.now().month)
    d = int(datetime.datetime.now().day)

    return (date(day=d, month=m, year=y).strftime('%A %d %B %Y'))


#Get Weather Based On Location
# Need to work on:
# Getting location based on real-time geo-location
# Getting weather for certain days
def getWeather(statement):
    location = 'Bournemouth'
    OpenWMap = OWM('API_KEY')
    mgr = OpenWMap.weather_manager()

    #Checks if user inputed "tomorrow" in statemnt and gets the weither for the next day.
    if "tomorrow" in statement: #//WIP//
        forecast = mgr.forecast_at_place((location,",GB"), 'daily')
        answer = forecast.will_be_clear_at(timestamps.tomorrow())
        print(answer)
        weather = answer

    #Gets current weather
    else:
        observation = mgr.weather_at_place(location+",GB")
        w = observation.weather

        wind = w.wind()['speed']
        status = w.detailed_status
        temp_max = round(w.temperature('celsius')['temp_max'])
        temp = round(w.temperature('celsius')['temp'])
        temp_min = round(w.temperature('celsius')['temp_min'])

        weather = "In {}, it's currently {} degrees with {}.".format(location, temp, status)

    return weather

#Opens different applications based on the input E.G. Google or Youtube. Formatted for MacOS.
def runOpen(inp):
    app = inp.split('open ')[-1]
    #Opens different websites
    if 'youtube' in app:
        webbrowser.open_new_tab("https://www.youtube.com")
        speak = ("youtube is now open")

    elif 'google' in app or 'chrome' in app:
        webbrowser.open_new_tab("https://www.google.com")
        speak = ("Google chrome is now open")

    elif 'gmail'in app:
        webbrowser.open_new_tab("https://mail.google.com/")
        speak = ("Google Mail open now")

    elif 'time table' in app or 'timetable' in app:
        speak = ("Now opening your timetable")
        open_new_tab('https://timetable.bournemouth.ac.uk/Student/Index')

    elif 'brightspace' in app:
        speak = ("Now opening BrightSpace")
        open_new_tab('https://brightspace.bournemouth.ac.uk/d2l/home')

    #Opens Mac Applications //Need to work on hwo fast it opens//
    else:
        speak=("Opening {}".format(app))
        os.system("""osascript -e 'tell app "{}" to open'""".format(app))

    return speak

def readFace(statemnt): #//WIP//
    name = fr.getFace()


#Volume Controls
def changeVolume(inp):
    #Checks to see if there is a number in the input and isolates it if there is.
    if any(num.isdigit() for num in inp):
        for word in inp.split():
            if word.isdigit():
                volume = int(word)

        #Increase sound by inpute value
        if "up" in inp and "by" in inp:
            code, out, err = osascript.osascript("output volume of (get volume settings)")
            diff = int(out) + volume
            print(type(int(out)), type(volume))
            osascript.osascript("set volume output volume {}".format(str((diff))))
            phrase = "changing volume to {}%".format(str(diff))

        #Decrease sound by inpute value
        elif "down" in inp and "by" in inp:
            code, out, err = osascript.run("output volume of (get volume settings)")
            diff = int(out) - volume
            osascript.osascript("set volume output volume {}".format(str((diff))))
            phrase = "changing volume to {}%".format(str(diff))

        #set vulome to input value
        else:
            osascript.osascript("set volume output volume {}".format(str(volume)))
            phrase = "changing volume to {}%".format(str(volume))

    # turn voluem up by 5
    elif "up" in inp:
        code, out, err = osascript.run("output volume of (get volume settings)")
        diff = int(out) + 5
        osascript.osascript("set volume output volume {}".format(str((diff))))
        phrase = "changing volume to {}%".format(str(diff))

    #turn voluem down by 5
    elif "down" in inp:
        code, out, err = osascript.run("output volume of (get volume settings)")
        diff = int(out) - 5
        osascript.osascript("set volume output volume {}".format(str((diff))))
        phrase = "changing volume to {}%".format(str(diff))
    
    #Mutes
    elif "mute" in inp:
        phrase = "Muting. You will no longer be able to hear me."
        osascript.osascript("set volume output volume 0")

    #gets current volume
    else:
        code, out, err = osascript.run("output volume of (get volume settings)")
        phrase= "Current Output Volume is at {}%".format(out)

    return phrase

#preforms basic google search to allow for things such as mathmatical questions, geogrpahical related questions and more
def search(statemnt):
    question = statemnt
    ssl._create_default_https_context = ssl._create_unverified_context

    app_id = "API_KEY"
    client = wolframalpha.Client(app_id)
    res = client.query(question)
    answer = next(res.results).text
    return answer

#Sportify Controls //WIP//
#lists all possible output devices
#enter the names of the devices here
list_devices = ["Devcie_Name", "Devcie_Name2"]

#This sets the active output device
def setDevice(device):
  #Get these details from the Spotify Dev Portal.
    data = {
  "client_id" : "",
  "client_secret" : "",
  "redirect_uri" : "",
  "scope" : "",
  "username" : "",
  "Active Device": device
}
    with open("spotify_cred.json", "w") as f:
        json.dump(data, f)
        print("cred Updated")

#defult device is Mac
setDevice(list_devices[0])

#Based on input can resume,skip and pause music
def controlSpotify(statment):#//WIP//

    with open("spotify_cred.json", "r") as f:
        data = json.load(f)

    auth_manager = SpotifyOAuth(
        client_id=data['client_id'],
        client_secret=data['client_secret'],
        redirect_uri=data['redirect_uri'],
        scope=data['scope'],
        username=data['username'])

    spotify = sp.Spotify(auth_manager=auth_manager)

    devices = spotify.devices()
    deviceID = None
    #Gets Devicew ID from Device Name
    for d in devices['devices']:
        dev = data["Active Device"].replace('’', '\'')
        d['name'] = d['name'].replace('’', '\'')
        if d['name'] == dev:
            deviceID = d['id']


    if "play" in statment or "resume" in statment or "next" in statment:
        Spotify.next_track(spotify=spotify, device_id=deviceID)
        phrase = "Playing next track"

    if "stop" in statment or "pause" in statment:
        Spotify.pause_playback(spotify=spotify, device_id=deviceID)
        phrase = "Spotify is now paused"

    return phrase

#Selects music to play.
def playSpotify(statement):

    with open("spotify_cred.json", "r") as f:
        data = json.load(f)

    auth_manager = SpotifyOAuth(
        client_id=data['client_id'],
        client_secret=data['client_secret'],
        redirect_uri=data['redirect_uri'],
        scope=data['scope'],
        username=data['username'])

    spotify = sp.Spotify(auth_manager=auth_manager)


    devices = spotify.devices()
    deviceID = None
    #Gets Devicew ID from Device Name
    for d in devices['devices']:
        dev = data["Active Device"].replace('’', '\'')
        d['name'] = d['name'].replace('’', '\'')
        if d['name'] == dev:
            deviceID = d['id']
            ActiveDev = deviceID

    #"play some Jay-Z" Plays music from that artist
    if "some" in statement:
        name = statement.split('some ')[-1]
        uri = get_artist_uri(spotify=spotify, name=name)
        play_artist(spotify=spotify, device_id=deviceID, uri=uri)
        phrase = "Now playing {}".format(name)

    #"Play Faded" plays the song faded
    elif "play" in statement:
        name = statement.split('play ')[-1]
        #checks if playlist is in the input string if it is it plays the playlist named faded
        if "playlist" in statement:
            uri = get_playlist_uri(spotify=spotify, name=name)
        else:
            uri = get_track_uri(spotify=spotify, name=name)
        play_track(spotify=spotify, device_id=deviceID, uri=uri)
        phrase = "Now playing {}".format(name)
    
    #changes output device to phone
    elif "phone" in statement:
        setDevice(list_devices[1])
        phrase = "Output device changed to your Phone"

    #changed output device to mac
    elif "mac" in statement:
        setDevice(list_devices[0])
        phrase = "Output device changed to your Mac"

    return phrase

#Shutdown computer
def shutdown(statement):
    print("shutting down...")
    system("shutdown /s /t 1")
