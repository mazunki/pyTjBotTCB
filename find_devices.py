import pyaudio
import json
p = pyaudio.PyAudio()
print("\n"*5)
for i in range(p.get_device_count()):
    print(json.dumps(p.get_device_info_by_index(i), indent=2))
    print("\n"*3)
