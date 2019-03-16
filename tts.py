from watson_developer_cloud import TextToSpeechV1 as tts 
from creds import credentials
import audioout

stt_creds = credentials["text_to_speech"]

tts_auth = tts(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])

def watson_play(play_text):
    print("playing audio...")
    print(play_text)
    watson_stream = tts_auth.synthesize(
        play_text, 
        "audio/l16;rate=44100"
    )
    
    synthetic_voice = watson_stream.get_result().content

    split_voice_segments = [synthetic_voice[i:i+16] for i in range(0,len(synthetic_voice),16)]

    for segment in split_voice_segments:
        print(segment)
        audioout.audio_stack_out.put(segment)
        print(audioout.audio_stack_out)

watson_play("potato is very good yes yes I agree I must eat more potato and kartoffel")

if __name__ == '__main__':
    watson_play("what song is that. darude sandstorm")
