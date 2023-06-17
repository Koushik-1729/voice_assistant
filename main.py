import speech_recognition as kr
import json
import pyttsx3
import datetime
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import tkinter as tk
import pygame
import os
import random
from mutagen.mp3 import MP3
from googlesearch import search
import itertools
import time

pygame.init()
pygame.mixer.init()

recognizer = kr.Recognizer()
engine = pyttsx3.init()
current_song_index = 0


volume = 0.5

shuffle_mode = False
repeat_mode = False

shuffle_mode = False
repeat_mode = False

MUSIC_DIRECTORY = "D:/music"
music_files = os.listdir(MUSIC_DIRECTORY)

def listen():
    with kr.Microphone() as source:
        print("Listening")
        recognizer.energy_threshold = 40000
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User Said: {query}")
        return query
    except kr.UnknownValueError:
        print("Sorry, I didn't understand. Can you please repeat?")
        return ""
    except kr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")
        return ""

def play_song():
    pygame.mixer.music.load(os.path.join(MUSIC_DIRECTORY, music_files[current_song_index]))
    pygame.mixer.music.play()
    exit()

def next_song(event=None):
    global current_song_index
    if shuffle_mode:
        current_song_index = random.randint(0, len(music_files) - 1)
    else:
        current_song_index = (current_song_index + 1) % len(music_files)
    play_song()

def prev_song(event=None):
    global current_song_index
    if shuffle_mode:
        current_song_index = random.randint(0, len(music_files) - 1)
    else:
        current_song_index = (current_song_index - 1) % len(music_files)
    play_song()


def pause_song():
    pygame.mixer.music.pause()

def unpause_song():
    pygame.mixer.music.unpause()

def stop_song():
    pygame.mixer.music.stop()

def decrease_volume():
    global volume
    if volume > 0.1:
        volume -= 0.1
        pygame.mixer.music.set_volume(volume)

def increase_volume():
    global volume
    if volume < 1.0:
        volume += 0.1
        pygame.mixer.music.set_volume(volume)

def speak(text):
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()


def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    response = f"The current time is {current_time}"
    speak(response)


def mobile_details():
    response = requests.get("http://ip-api.com/json")
    data = json.loads(response.content)
    country = data["country"]
    city = data["city"]
    region = data["region"]
    isp = data["isp"]
    response = f"You are in {city}, {region}, {country}. Your ISP is {isp}"
    speak(response)

def web_search(query):
    response = "Let me search that for you."
    speak(response)
    results = list(search(query, num_results=10))

    if results:
        response = "Here are some search results:"
        speak(response)
        limited_results = results[:5]  # Limit the number of results to 5
        for i, result in enumerate(limited_results, start=1):
            speak(f"Result {i}: {result}")
    else:
        response = "Sorry, I couldn't find any relevant results for your search."
        speak(response)
        

def process_query(query):
    if "hello" in query:
        response = "Hey! What's your name?"
        speak(response)
        name = listen()  # Capture the user's name
        response = f"Nice to meet you, {name}! How can I assist you?"
    elif "time" in query:
        get_time()
    elif "mobile details" in query:
        mobile_details()
    elif "play music" in query:
        play_song()
    elif "pause song" in query:
        pause_song()
    elif "next song" in query:
        next_song()
    elif "previous song" in query:
        prev_song()
    elif "unpause song" in query:
        unpause_song()
    elif "stop song" in query:
        stop_song()
    elif "increase volume" in query:
        increase_volume()
    elif "decrease volume" in query:
        decrease_volume()
    elif "search" in query:
        search_query = query.split("search")[-1].strip()
        if search_query:
            web_search(search_query)
        else:
            response = "Please provide a search query."
            speak(response)
    elif "stop" in query:
        response = "As you requested. Goodbye!"
        speak(response)

    else:
        response = "I'm sorry, I don't have the requested information"
        speak(response)

while True:
    query = listen()
    time.sleep(1)  # Add a delay of 1 second
    process_query(query)