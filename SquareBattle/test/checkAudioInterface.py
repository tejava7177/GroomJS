# import pyaudio
#
# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(f"ID {i}: {info['name']} - 입력 채널: {info['maxInputChannels']}")
# p.terminate()


import sounddevice as sd

print("🔍 사용 가능한 오디오 장치 목록:")
device_list = sd.query_devices()
print(device_list)