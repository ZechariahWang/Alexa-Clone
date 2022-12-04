# Import AI modules
import flask
import googletrans
import speech_recognition as sr
import pyttsx3
import asyncio
# Import command modules
import pywhatkit
import datetime
import wikipedia
import pyjokes
import python_weather
import requests
# Misc modules
import time
import random
import math

# Init phase
recognizer = sr.Recognizer()
translator = googletrans.Translator()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Conditional variables
StandardCondition = True
InUse = False
text = ""
api_key = "620e1da16bee621feb088d3c65166b89" # api key this might be kinda important idk

# get api data
weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q=Calgary&units=metric&APPID={api_key}")

# Bot settings
Name = "siri"


# Weather database. Will need to add more cities in the future
cities = ["calgary",
          "edmonton",
          "toronto",
          "vancouver",
          "burnaby",
          "taipei",
          "dallas",
          "houston"]

# Response database
responses = ["I'm good, hope you are doing good as well!",
             "I'm doing great! Wishing you the same.",
             "I'm fine I guess. It could be worse. At least I'm not Sarah.",
             "Valorant sucks it makes me wanna commit.",
             "Life makes me want to play league",
             "I just wanna cry. No one will ever love me. Oh wait a minute. Its because I play Valorant.",
             "I'm gonna be alone for the rest of my life. What am I doing bro."]


# Invalid response database
invalidresponses = ["Sorry, I didn't get that.",
                    "I'm sorry, I don't understand.",
                    "Are you physically disabled? Speak clearly lol."]


# Helper functions cause idk whats going on

# Speak message
def OutputVoice(message):
    engine.say(message)
    engine.runAndWait()
    print(message)
    return

# Global function to change voice of AI
def ChangeVoice(id):
    engine.say("Voice is being set to type:")
    engine.runAndWait()
    engine.setProperty("voice", voices[id].id)
    engine.say(id)
    engine.runAndWait()
    return

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False


def GetWeather(city):
    global weather_data

    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}")

    weather = weather_data.json()['weather'][0]['main']
    temp = weather_data.json()['main']['temp']
    OutputVoice("Currently in " + city + ", it is " + str(round(temp)) + " degrees celsius with " + str(weather))
    return


# Primary Command Classes for stuff idk how it works lol

class InvalidResponseClass:
    def __init__(self, response):
        self.response = response

    def reply(self):
        replyint = random.uniform(0, len(invalidresponses))
        roundedreply = math.floor(replyint)
        OutputVoice(invalidresponses[roundedreply])


class PersonalResponses:
    def __init__(self, command):
        self.command = command

    def Response(self):
        randomresponse = random.uniform(0, len(responses))
        response = math.floor(randomresponse)
        print(responses[response])
        OutputVoice(responses[response])

# Weather Class
class WeatherData:
    def __init__(self, weatherinfo):
        self.city = weatherinfo

    def DisplayWeather(self):
        global weather_data

        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&APPID={api_key}")

        weather = weather_data.json()['weather'][0]['main']
        temp = weather_data.json()['main']['temp']
        OutputVoice("Currently in " + self.city + ", it is " + str(round(temp)) + " degrees celsius with " + str(weather))
        return

# Wikipedia Class
class WikipediaInfo:
    def __init__(self, wikipedia):
        self.wikipedia = wikipedia

    def WikipediaSummary(self):
        object = self.wikipedia.replace("according wikipedia", "")
        object = self.wikipedia.replace("Who is", "")
        info = wikipedia.summary(object, 3)
        OutputVoice(info)

# Clock Class
class Clock:
    def __init__(self, time):
        self.time = time

    def TellTime(self):

        hour = int(datetime.datetime.now().strftime("%H"))
        minutes = int(datetime.datetime.now().strftime("%M"))
        if hour > 12:
            reformattedtime = hour - 12
            time = reformattedtime
            updatedmessage = ("The current time is: " + str(time) + ":" + str(datetime.datetime.now().strftime("%M")))
            OutputVoice(updatedmessage)
        else:
            time = datetime.datetime.now().strftime("%H:%M")
            updatedmessage = ("The current time is: " + str(time))
            OutputVoice(updatedmessage)

# Video/Music class
class Play_Video:
    def __init__(self, command):
        self.command = command

    def PlayVid(self):

        command = self.command.replace("play", "")
        command = self.command.replace("siri", "")
        updatedmessage = ("Playing" + command + "on Youtube")
        OutputVoice(updatedmessage)
        pywhatkit.playonyt(command)

# Change speaker voice class
class VoiceClass:
    def __init__(self, id):
        self.id = id

    def ChangeVoice(self):
        engine.say("Voice is being set to type:")
        engine.runAndWait()
        engine.setProperty("voice", voices[self.id].id)
        engine.say(self.id)
        engine.runAndWait()
        return

# Intake user command
def InputCommand():
    global text
    try:
        with sr.Microphone() as source:
            print('Currently Active, say something!')
            recognizer.adjust_for_ambient_noise(source)
            voice = recognizer.listen(source)

            text = recognizer.recognize_google(voice)
            text = text.lower()
            if text:
                print("Input has been detected")

            else:
                print("Gone, just like my dad")
            time.sleep(0.10)
    except:
        pass
    return text


# Detection to figure out what is within the message
def CommandInput():
    global text
    global InUse

    InUse = True
    command = InputCommand()
    print("User command given: ", command)

    # Play check
    if "play" in command and Name in command:
        vid = Play_Video(command)
        vid.PlayVid()

    # Time check
    elif "time" in command and Name in command:
        timeclass = Clock(time)
        timeclass.TellTime()

    # Weather check
    elif "weather" in command and Name in command:
        for i in cities:
            print(i)
            if i in command:
                weatherclass = WeatherData(i)
                weatherclass.DisplayWeather()
                break
            else:
                pass

    # Wikipedia check
    elif "according to wikipedia" in command:
        wikipediaclass = WikipediaInfo(command)
        wikipediaclass.WikipediaSummary()

    # Joke check
    elif "joke" in command or "jokes" in command and Name in command:
        OutputVoice(pyjokes.get_joke())

    # Voice type check
    elif "voice" in command and "type 1" in command and Name in command:
        voice = VoiceClass(1)
        voice.ChangeVoice()

    elif "voice" in command and "type 0" in command and Name in command:
        voice = VoiceClass(0)
        voice.ChangeVoice()
    # Personality Response questions
    elif "how are you" in command and Name in command:
        responseclass = PersonalResponses(command)
        responseclass.Response()

    # Command is not detected as valid
    elif Name in command:
        InvalidReply = InvalidResponseClass(command)
        InvalidReply.reply()

    else:
        print("Not valid just like me")

    time.sleep(0.1)
    text = ""


# Main control function
def main():
    while True:
        CommandInput()
        time.sleep(0.1)


# Call main
main()

