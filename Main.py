import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import smtplib
import os

# Initialize the TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. How may I help you?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
        return query.lower()
    except Exception:
        print("Could you please say that again?")
        speak("Could you please say that again?")
        return "none"

def send_email(to, content):
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('EMAIL_PASSWORD')
    if not EMAIL or not PASSWORD:
        speak("Email credentials are not set. Please set your environment variables.")
        return

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to, content)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I was not able to send the email.")

if __name__ == "__main__":
    greet()
    while True:
        query = take_command()

        if query == "none":
            continue

        if "wikipedia" in query:
            try:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "").strip()
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception:
                speak("Sorry, I couldn't find any results on Wikipedia.")

        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "time" in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif "email to john" in query:
            speak("What should I say?")
            content = take_command()
            if content != "none":
                to = "john.doe@example.com"
                send_email(to, content)
            else:
                speak("Email content was empty, email not sent.")

        elif "exit" in query or "quit" in query:
            speak("Goodbye. Have a nice day!")
            break
