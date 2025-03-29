import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized command: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the command.")
            return None
        except sr.RequestError:
            print("Speech Recognition service is unavailable.")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None

def process_command(command):
    if command in ["forward", "move forward", "go ahead"]:
        speak("Moving forward")
        # Send motor command here
    elif command in ["backward", "move back", "reverse"]:
        speak("Moving backward")
        # Send motor command here
    elif command in ["left", "turn left"]:
        speak("Turning left")
        # Send motor command here
    elif command in ["right", "turn right"]:
        speak("Turning right")
        # Send motor command here
    elif command in ["stop", "halt"]:
        speak("Stopping")
        # Send stop command here
    else:
        speak("Unknown command")

if __name__ == "__main__":
    while True:
        command = recognize_command()
        if command:
            process_command(command)
