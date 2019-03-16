import stt
import audioout
import audioin
from threading import Thread

if __name__ == "__main__":
    
    th_audio_out = Thread(target=audioout.audio_from_stack)
    th_audio_in =  Thread(target=audioin.audio_to_stack)
    th_watson_stt_socket = Thread(target=stt.stt_ws)
    #th_tone_analyze = Thread()
    
    th_audio_out.not_stopped = True
    th_audio_out.not_stopped = True

    th_audio_out.start()
    th_audio_in.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        th_audio_out.not_stopped = False
        th_audio_in.not_stopped = False
    
    #stt.watson_stt()
