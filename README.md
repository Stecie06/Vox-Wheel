# Vox-Wheel

Vox-Wheel: Voice-Controlled IoT Wheelchair

Overview

Vox-Wheel is an intelligent, IoT-powered wheelchair designed to enhance mobility for people with disabilities. It supports multiple control options, including voice commands, joystick input, and obstacle detection to ensure safe navigation. The wheelchair also features multilingual support and user voice recognition for personalized operation.

Features

Voice-Controlled Navigation: Move forward, backward, turn left, right, or stop using voice commands.

User Voice Recognition: Identifies and verifies the registered user before executing commands.

Joystick Support: Users can switch between voice control and joystick mode.

Obstacle Detection: Automatically stops movement if an obstacle is detected.

Multilingual Support: Users can change the control language to their preferred choice.

Hardware Requirements

Raspberry Pi

Motor Driver Module

2 DC Motors

Ultrasonic Sensor (for obstacle detection)

Microphone (for voice commands)

Joystick (for manual control)

Software Requirements

Python 3

speech_recognition (for voice input)

pyttsx3 (for text-to-speech conversion)

googletrans (for language translation)

pygame (for joystick integration)

RPi.GPIO (for motor control)

Installation

Clone this repository:

git clone https://github.com/your-username/Vox-Wheel.git
cd Vox-Wheel

Install dependencies:

pip install speechrecognition pyttsx3 googletrans pygame RPi.GPIO

Run the program:

python main.py

How to Use

Register Your Voice: Say "Register my voice" to store your unique voice pattern.

Switch Control Mode: Say "Switch to joystick" to use manual control.

Change Language: Say "Set language to [desired language]".

Navigation Commands:

"Move forward"

"Move backward"

"Turn left"

"Turn right"

"Stop"

Safety Precautions

Ensure the motors and power supply are properly connected.

Test in an open space before using in a real-world environment.

Avoid high-speed movements in tight areas.