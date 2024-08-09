import pyttsx3
import requests
import speech_recognition as sr
import datetime as dt
import wikipedia
import pywhatkit
import webbrowser
import pyautogui
import os

from openai.api_resources import completion
from pynput.keyboard import Key,Controller
from time import sleep
import openai
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def takecommand():
    tc = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening to your voice")
        tc.pause_threshold = 1
        tc.energy_threshold = 300
        audio = tc.listen(source, 0, 4)
    try:
        print("I am trying to understand your command")
        query = tc.recognize_google(audio, language="en-in")
        print(f"did u mean {query}\n")
    except:
        print("sorry i didnt get that can u please repeat it again ")
    return query
def greet():
    hour = int(dt.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("good morning,by the way i am friday")
    elif hour>=12 and hour<=18:
        speak("good afternoon,by the way i am friday")
    elif hour>=18 and hour<=21:
        speak("good evening,by the way i am friday")
    elif hour>=21 and hour<=24:
        speak(" good night ,by the wayi am friday")
    speak("please tell me how can i help you")
def google_search(query):
    if "google" in query:
        import wikipedia as googlescrap
        query = query.replace("friday", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        speak("this is what i found on google")
        try:
            pywhatkit.search(query)
            result = googlescrap.summary(query,1)
            print(result)
        except:
            speak("no speakable output")
def youtube_search(query):
    if "youtube" in query:
        speak("this is what i found")
        query = query.replace("friday", "")
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("done")
def wiki_search(query):
    if "wikipedia" in query:
        speak("this is what i found")
        query = query.replace("friday", "")
        query = query.replace("wikipedia search", "")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=6)
        print(result)
def openappweb(query):
    speak("Launching")
    query = query.replace("open", "")
    query = query.replace("friday", "")
    pyautogui.press("super")
    pyautogui.typewrite(query)
    pyautogui.sleep(2)
    pyautogui.press("enter")

openai.api_key="get your own api key"
def Reply(question):
    prompt = f'vishal: {question}\n friday: '
    response = completion.create(prompt=prompt, engine="text-davinci-002", stop=['\vishal'], max_tokens=200)
    answer = response.choices[0].text.strip()
    return answer
dic={"commandprompt":"cmd","paint":"paint","word":"winword","excel":"excel","chrome":"chrome","spotify":"spotify","twitter":"twitter","whatsapp":"whatsapp","pycharm":"pycharm"}
def closeappweb(query):
    speak("Closing")
    if "one tab" in query or "1 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed")
    elif "2 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed")
    elif "3 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed")

    elif "4 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed")
    elif "5 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "w")
        speak("All tabs closed")

    else:
        keys = list(dic.keys())
        for app in keys:
            if app in query:
                os.system(f"taskkill /f /im {dic[app]}.exe")
keyboard = Controller()

def volumeup():
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)
def volumedown():
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)
        
def weather_info():
    api_key = "your-openweathermap-api-key"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("Please tell me the city name")
    city_name = takecommand().lower()
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]
        weather_report = f"Temperature: {temperature}°C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nDescription: {description}"
        print(weather_report)
        speak(weather_report)
    else:
        speak("City not found. Please try again.")


def set_reminder(notification=None):
    speak("What shall I remind you about?")
    reminder_text = takecommand()
    speak("In how many minutes should I remind you?")
    reminder_time = int(takecommand())
    sleep(reminder_time * 60)
    speak(f"Reminder: {reminder_text}")
    notification.notify(title="Reminder", message=reminder_text, timeout=10)


def news_update():
    api_key = "your-newsapi-org-api-key"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data["articles"]
    speak("Here are the top news headlines:")
    for i, article in enumerate(articles[:5], start=1):
        print(f"{i}. {article['title']}")
        speak(article["title"])
        if i < 5:
            speak("Next headline...")
        else:
            speak("That’s all for now.")


if __name__ == "__main__":
    while True:
        query = takecommand().lower()
        if "wake up" in query:
            greet()
            while True:
                query = takecommand().lower()
                if "go to sleep" in query:
                    speak("Okay, you can call me any time.")
                    break
                elif "hello" in query:
                    speak("Hello! How can I help you?")
                elif "i am fine" in query:
                    speak("Great to hear that!")
                elif "how are you" in query:
                    speak("I'm great!")
                elif "thank you" in query:
                    speak("You're welcome, mate!")
                elif "google" in query:
                    google_search(query)
                elif "youtube" in query:
                    youtube_search(query)
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("Video paused.")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("Video playing.")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("Video muted.")
                elif "volume up" in query:
                    volumeup()
                    speak("Volume increased.")
                elif "volume down" in query:
                    volumedown()
                    speak("Volume decreased.")
                elif "wikipedia" in query:
                    wiki_search(query)
                elif "open" in query:
                    openappweb(query)
                elif "close" in query:
                    closeappweb(query)
                elif "shut down" in query:
                    speak("Are you sure you want to shut down the system?")
                    ans = takecommand().lower()
                    if "yes" in ans:
                        os.system("shutdown /s /t 1")
                    else:
                        speak("Shut down cancelled.")
                elif "gpt" in query:
                    query = query.replace("friday", "").replace("gpt", "")
                    answer = Reply(query)
                    speak(answer)
                    print(answer)
                elif "weather" in query:
                    weather_info()
                elif "remind me" in query:
                    set_reminder()
                elif "news" in query:
                    news_update()
                elif "finally sleep" in query:
                    speak("going to sleep")
                    exit()







