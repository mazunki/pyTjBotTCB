# pyTjBotTCB
A repository for The Circuit Breakers at Noroff, creating a TJBot in Python.

## Credentials

In order for any of the services to work, credentials in the form of API keys/tokens need to be added to `creds.json`. These are given on the Dashboard of Bluemix.

Support for a username/password combination for this service is not supported by this application by default, since it is a deprecated feature by defintion of IBM Watson; and will therefore never be added here. If needed, modify `stt.py`.


## Speech to text

Requiring to install pyaudio in order to work with `python -m pip install pyaudio`, stt.py allows the user to receive text from IBM Watson's SpeechToText service.

In order to handle this, `/audioin.py` is used, which can also record and save a .wav file to the current folder with the `file_stt()` function.
