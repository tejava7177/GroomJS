import sounddevice as sd
import numpy as np
import soundfile as sf

samplerate = 48000  # BlackHole 기본 샘플링 속도
channels = 2
duration = 15  # 녹음 시간 (5초)

print("🎤 테스트 녹음 시작...")

# ✅ BlackHole 장치 ID 찾기
devices = sd.query_devices()
blackhole_device = None
for i, device in enumerate(devices):
    if "BlackHole" in device["name"] and device.get("max_input_channels", 0) > 0:
        blackhole_device = i
        break

if blackhole_device is None:
    print("❌ BlackHole 오디오 장치를 찾을 수 없습니다.")
else:
    print(f"✅ 'BlackHole' 오디오 장치 선택됨: ID {blackhole_device}")

    # ✅ BlackHole을 통해 5초간 녹음 테스트
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype="int16", device=blackhole_device)
    sd.wait()  # ✅ 녹음 완료될 때까지 대기

    # ✅ 녹음된 데이터 확인
    if np.any(audio_data):
        print("✅ 오디오 데이터가 정상적으로 녹음됨.")
        sf.write("test_audio.wav", audio_data, samplerate)
        print("✅ 'test_audio.wav' 파일이 생성됨.")
    else:
        print("⚠️ 녹음된 데이터가 없습니다.")