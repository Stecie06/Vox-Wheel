import speech_recognition as sr
import pyttsx3
import RPi.GPIO as GPIO
import time
from googletrans import Translator

# Motor GPIO Pins
MOTOR_LEFT_FORWARD = 17
MOTOR_LEFT_BACKWARD = 18
MOTOR_RIGHT_FORWARD = 22
MOTOR_RIGHT_BACKWARD = 23

# Ultrasonic Sensor Pins
TRIG = 24
ECHO = 25

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

translator = Translator()
selected_language = "en"  # Default language is English

def speak(text):
    engine = pyttsx3.init()
    translated_text = translator.translate(text, dest=selected_language).text
    engine.say(translated_text)
    engine.runAndWait()

def recognize_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio, language=selected_language).lower()
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

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
    
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Distance in cm
    return distance

def move_forward():
    if measure_distance() > 20:  # Move only if obstacle is not close
        GPIO.output(MOTOR_LEFT_FORWARD, True)
        GPIO.output(MOTOR_RIGHT_FORWARD, True)
        GPIO.output(MOTOR_LEFT_BACKWARD, False)
        GPIO.output(MOTOR_RIGHT_BACKWARD, False)
    else:
        speak("Obstacle detected, stopping")
        stop()

def move_backward():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, True)
    GPIO.output(MOTOR_RIGHT_BACKWARD, True)

def turn_left():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, True)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

def turn_right():
    GPIO.output(MOTOR_LEFT_FORWARD, True)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

def stop():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

def process_command(command):
    global selected_language
    if command in ["forward", "move forward", "go ahead"]:
        speak("Moving forward")
        move_forward()
    elif command in ["backward", "move back", "reverse"]:
        speak("Moving backward")
        move_backward()
    elif command in ["left", "turn left"]:
        speak("Turning left")
        turn_left()
    elif command in ["right", "turn right"]:
        speak("Turning right")
        turn_right()
    elif command in ["stop", "halt"]:
        speak("Stopping")
        stop()
    elif command.startswith("set language to"):
        new_language = command.replace("set language to", "").strip()
        speak(f"Changing language to {new_language}")
        selected_language = new_language
    else:
        speak("Unknown command")

if __name__ == "__main__":
    try:
        while True:
            command = recognize_command()
            if command:
                process_command(command)
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()