from watson_developer_cloud import TextToSpeechV1 as tts 
from creds import credentials
from audioout import play_audio

stt_creds = credentials["text_to_speech"]

tts_auth = tts(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])

def watson_play(play_text):
    print("playing audio...")
    print(play_text)
    watson_stream = tts_auth.synthesize(play_text, 
                                        "audio/wav"
                                        )
    synthetic_voice = watson_stream.get_result().content

    with open("output_file.wav", "wb") as audio_file:
        audio_file.write(synthetic_voice)
    
    play_audio("output_file.wav")

if __name__ == '__main__':
    watson_play("what song is that. darude sandstorm")
