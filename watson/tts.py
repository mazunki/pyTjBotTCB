"""
Allows a string of text to be transformed into audio through Watson's services.
"""
from watson_developer_cloud import TextToSpeechV1 as wtts
from creds import credentials
import audio.audioout as audioout

stt_creds = credentials["text_to_speech"]

tts_auth = wtts(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])

def watson_play(play_text):
    """
    Sends the input string to Watson and returns a message to the speaker.
    """
    print("Sending text to watson... \"",play_text,"\"",sep="")
    watson_stream = tts_auth.synthesize(
        play_text, 
        "audio/l16;rate=88200"
    )
    
    synthetic_voice = watson_stream.get_result().content

    return audioout.play_audio(synthetic_voice)

if __name__ == '__main__':
    import sys.path
    sys.path.insert(0,"../")
    watson_play("what song is that. darude sandstorm")
