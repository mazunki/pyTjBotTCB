# pyTjBotTCB
A repository for The Circuit Breakers at Noroff, creating a TJBot in Python.

## Credentials

In order for any of the services to work, credentials in the form of API keys/tokens need to be added to `creds.json`. These are given on the Dashboard of Bluemix.

Support for a username/password combination for this service is not supported by this application by default, since it is a deprecated feature by defintion of IBM Watson; and will therefore never be added here. If needed, modify on a fork.


## Speech to text

Requiring to install pyaudio in order to work with `python3 -m pip install pyaudio`, stt.py allows the user to receive text from IBM Watson's SpeechToText service, installed with `python3 -m pip install watson_developer_cloud`.

While tts.tts_file() streams a file to Watson, `stt.stt_ws_listener()` will listen forever for audio on the microphone (actually from a FIFO stack, filled by the mic). Audio files can be recorded on need with `audioin.record_file()`

## Text to Speech

By inputting a string to `tts.watson_play()` the sound will be played on the audio output interface. Playing audio simultaneously makes the audio minced, but isn't a major issue. 

Playing audiofiles is possible with `audioout.play_file()`
