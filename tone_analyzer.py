from watson_developer_cloud import ToneAnalyzerV3 as toneanal

import json

from creds import credentials
import tts

tone_anal_creds = credentials["tone_analyzer"]
tone_anal = toneanal(
        version="2019-03-11",  # This is stupid, but necessary lol
        iam_apikey=tone_anal_creds["api_key"],
        url=tone_anal_creds["url"]
        )

sample_text = "I am really pissed at you now. You could have done better. Do you really think you could get away with what you have done? You ignorant piece of shit."

def analyse_text(text=sample_text, num_tones=1): # 7 is the currently highest number of tones

    print("analysing tone...", text)
    data_to_analyze = {
            "text": text
            }
    print(data_to_analyze)

    tone_analysis = tone_anal.tone(data_to_analyze, "application/json").get_result()

    #print("TONE: \n====================\n"+tone_analysis)
    if num_tones == 1:
        confidence = 0.0 # API only returns >0.5 tones anyway
        for item in tone_analysis["document_tone"]["tones"]:
            print(item)
            if item["score"] > confidence:
                confidence = item["score"]
                tone = item["tone_name"] # tone_id or tone_name?
                #print(confidence,tone) 
        if confidence == 0.0:
            return "emotionless", "1"  # hacky lol, returns this if watson doesn't return any tone
        else:
            print(tone,confidence)
            return str(tone), str(confidence)
    else:
        return tone_analysis["document_tone"]["tones"]

if __name__ == "__main__":
    tone, confidence = analyse_text("I am very angry with you right now")
    print(tone, "with", confidence, "confidence.")


