# Imports
import json
import os
import pickle
from importlib import reload

# Chat related
import colorama

# AI Training
import numpy as np
import pyttsx3
import speech_recognition as sr
from colorama import Fore, Style
from tensorflow import keras

# Brains
import Gideon_Brains

# Settig TTS Voice to female
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', "com.apple.speech.synthesis.voice.karen.premium")
engine.setProperty('rate', 950)

colorama.init()

# Loading given intents
with open("intents.json") as file:
    data = json.load(file)


def speak(audio):
    print(Fore.GREEN + "Gideon:" + Style.RESET_ALL, audio)
    engine.say(audio)
    engine.runAndWait()
    engine.stop()


def take_command():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            print('Recognizing...')
            qry = r.recognize_google(audio, language='en-in')
            print(qry)
            return qry

        #     if any error occurs this line will run
        except:
            # if you don't want to print the error comment the bottom line
            print('Say that again please\n')


def chat():
    # load trained model
    model = keras.models.load_model('train/chat_model')

    # load tokenizer object
    with open('train/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('train/label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20

    speak(Gideon_Brains.wishme())

    wake_word = "gideon"
    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        # inp = take_command().lower() #Uncomment this for voice input and comment the line below
        inp = input().lower() 
        
        if "quit" in inp.lower(): #Quits out of prgram 
            quit()
            
        elif "retrain" in inp: #Retrains the model for anu changes ot the intents while program is running
            speak("Updating Dictionary. Please bear with me")
            os.system('python train.py')
            
        elif "reload" in inp and "systems" in inp: #Updates functions used for Gideon
            speak("Reloading Modules. Please Wait")
            reload(Gideon_Brains)

        elif "search" in inp: #This is basically google search, had to do its own key word to run properly with the intents //WIP//
            speak(Gideon_Brains.search(inp))

        else: #This generates a resaponsed based on the trained model and the intents.
            result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                                              truncating='post', maxlen=max_len))
            tag = lbl_encoder.inverse_transform([np.argmax(result)])
            
            
            for i in data['intents']:
                if i['tag'] == tag:
                    # Cheks if the intent given has a function tied to it E.G. "Whats the time" will preform the getTime function.
                    #If the funtion intent is empty it will just pick a response to fit the inpute
                    if i['function'] != '':
                        print(i['function'])
                        if i['responses'] != []:
                            speak(np.random.choice(i['responses']))
                        func = getattr(Gideon_Brains, i['function']) #runs the function from the Brains and speaks the answer.
                        speak(func(inp))
                        
                    else:
                        choice = np.random.choice(i['responses'])
                        speak(choice)

if __name__ == '__main__':
    print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)
    chat()
