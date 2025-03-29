import speech_recognition as sr
import pyttsx3
import RPi.GPIO as GPIO

# Motor GPIO Pins
MOTOR_LEFT_FORWARD = 17
MOTOR_LEFT_BACKWARD = 18
MOTOR_RIGHT_FORWARD = 22
MOTOR_RIGHT_BACKWARD = 23

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)

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

def move_forward():
    GPIO.output(MOTOR_LEFT_FORWARD, True)
    GPIO.output(MOTOR_RIGHT_FORWARD, True)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

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
