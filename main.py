import speech_recognition as kr
import json
import pyttsx3
import datetime
import requests

recognizer=kr.Recognizer()

engine=pyttsx3.init()


def listen():
    with kr.Microphone() as source:
        print("Listining")
        recognizer.energy_threshold = 40000
        audio=recognizer.listen(source)

    try:
        print("Reconizing.........")
        query=recognizer.recognize_google(audio)
        print(f"User Said:{query}")
        return query
    except Exception as e:
        print("Sorry I didn't understand. Can you please repeat?")
        return " "
    


def speak(text):
    engine.setProperty("rate",150)
    engine.say(text)
    engine.runAndWait()


def get_time():
    now=datetime.datetime.now()
    current_time=now.strftime("%I:%M %p")
    response=f"The current time is {current_time}"
    speak(response)


def mobile_details():
    response=requests.get("http://ip-api.com/json")
    data=json.loads(response.content)
    country=data["country"]
    city=data["city"]
    region=data["region"]
    isp=data["isp"]
    response=f"you are in{city},{region},{country}.Your ISP is {isp}"
    speak(response)


def process_query(query):
    if "hello" in query:
        response = f"Hey! What's your name?"
        speak(response)
        name = listen()  # Capture the user's name
        response = f"Nice to meet you, {name}! How can I assist you?"
    elif "time" in query:
      current_time = datetime.datetime.now().strftime("%I:%M %p")
      response = f"The current time is {current_time}"
    elif "mobile details" in query:
        response = mobile_details()

    elif "stop" in query:
      response="As you requested"
      speak(response)
      exit()  # Stop the program execution

    else:
        response="I'm sorry,I don't have requested Information"
    speak(response)
while True:
    query=listen()
    process_query(query)

            

