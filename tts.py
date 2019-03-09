from watson_developer_cloud import TextToSpeechV1 as tts 
from creds import credentials
from audioout import play_audio

stt_creds = credentials["text_to_speech"]

tts_auth = tts(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])

def watson_play(play_text):
    with open("output_file.wav", "wb") as audio_file:
        audio_file.write(
            tts_auth.synthesize(
                play_text, "audio/wav"
            ).get_result().content
        )
    
    play_audio("output_file.wav")