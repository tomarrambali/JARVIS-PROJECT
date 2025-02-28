import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import pyttsx3  # Import pyttsx3 for text-to-speech
import numpy as np

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Wrap this inside of a try-catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Wrap this inside of a try-catch block
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    # Use pyttsx3 for text-to-speech on Windows
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        print("Listening...")
        query = takeCommand()

        # Open different sites based on the command
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"], ["video", "https://youtu.be/J7Oj4VdBxWQ?si=ZnrWVyx4SbdHfr6w"], ["music", "C:\\Users\\RAMBALI SINGH TOMAR\\Music\\Setho Ka Seth.mp3"] ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        # Play music if the command is given
        if "open music" in query:
            musicPath = "/path/to/music.mp3"
            os.system(f"open {musicPath}")

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {min} minutes.")

        elif "open facetime" in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass" in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "Using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit" in query.lower():
            exit()

        elif "reset chat" in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
