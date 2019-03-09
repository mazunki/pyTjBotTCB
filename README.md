# pyTjBotTCB
A repository for The Circuit Breakers at Noroff, creating a TJBot in Python.

## Speech to text

Requiring to install pyaudio in order to work with python -m pip install pyaudio, stt.py allows the user to receive text from IBM Watson's SpeechToText service.

In order to handle this, /audioin.py is used, which can also record and save a .wav file to the current folder with the file_stt() function.
