import cv2
import pygame
import numpy as np
import sounddevice as sd
import soundfile as sf
import threading
import subprocess
import os

class GameRecorder:
    def __init__(self, screen, output_filename="gameplay.mp4", fps=30):
        """ 게임 화면과 사운드를 동시에 녹화하는 클래스 """
        self.screen = screen
        self.fps = fps
        self.output_filename = output_filename
        self.audio_filename = "audio.wav"  # ✅ 녹음할 오디오 파일
        self.converted_filename = "gameplay_with_audio.mp4"  # ✅ 최종 변환된 파일
        self.video_writer = None
        self.recording = False
        self.audio_thread = None  # 오디오 녹음용 스레드
        self.samplerate = 44100
        self.channels = 2

    def start_recording(self):
        """ 녹화 시작 (비디오 + 오디오) """
        print(f"🎥 녹화 시작! 파일 저장: {self.output_filename}")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(self.output_filename, fourcc, self.fps, (self.screen.get_width(), self.screen.get_height()))

        if not self.video_writer.isOpened():
            print("❌ 오류: 비디오 파일을 생성할 수 없습니다.")
            return

        self.recording = True
        print("🎤 녹음 스레드 실행")
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.audio_thread.start()

    def capture_frame(self):
        """ 현재 Pygame 화면을 캡처하여 OpenCV 포맷으로 변환 후 저장 """
        if self.recording and self.video_writer and self.video_writer.isOpened():
            pygame_surface = pygame.display.get_surface()
            frame = pygame.surfarray.array3d(pygame_surface)

            if frame is None:
                print("⚠️ 캡처된 프레임이 None입니다. 녹화를 중단합니다.")
                return

            frame = np.rot90(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.video_writer.write(frame)

    def stop_recording(self):
        """ 녹화 중지 및 저장 + 오디오 녹음 종료 + 비디오-오디오 합치기 """
        if self.recording:
            self.recording = False
            self.video_writer.release()
            print(f"🎬 녹화 완료! {self.output_filename} 저장됨.")

            # ✅ 오디오 녹음 종료
            self.audio_thread.join()
            print("🎤 오디오 녹음 완료!")

            # ✅ 비디오 + 오디오 결합
            self.merge_audio_video()

    def record_audio(self):
        """ Pygame에서 실행되는 시스템 사운드를 직접 녹음 (Mac 환경) """
        samplerate = 44100  # ✅ 오디오 샘플링 속도
        channels = 2  # ✅ 스테레오 녹음
        duration = 60  # ✅ 녹음 길이 (초)

        print("🎤 시스템 사운드 녹음 시작...")

        # ✅ BlackHole이 올바르게 설치되었는지 확인
        devices = sd.query_devices()
        blackhole_device = None
        for i, device in enumerate(devices):
            if "BlackHole" in device["name"]:
                blackhole_device = i
                break

        if blackhole_device is None:
            print("❌ 'BlackHole' 오디오 장치를 찾을 수 없습니다.")
            return

        print(f"✅ 'BlackHole' 오디오 장치 선택: ID {blackhole_device}")

        # ✅ BlackHole을 통해 시스템 사운드 녹음
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype="int16",
                            device=blackhole_device)
        sd.wait()
        print("🎤 녹음 완료!")

        # ✅ WAV 파일로 저장
        sf.write(self.audio_filename, audio_data, samplerate)
        print(f"✅ 오디오 파일 저장 완료: {self.audio_filename}")

    def merge_audio_video(self):
        """ FFmpeg를 사용하여 비디오와 오디오를 합침 """
        if not os.path.exists(self.audio_filename):
            print("❌ 오디오 파일이 존재하지 않습니다. 비디오만 저장됩니다.")
            return

        print(f"🔄 FFmpeg로 {self.converted_filename} 변환 중...")

        command = [
            "ffmpeg", "-i", self.output_filename,  # ✅ 비디오 입력
            "-i", self.audio_filename,  # ✅ 오디오 입력
            "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental",  # ✅ 비디오 & 오디오 설정
            self.converted_filename
        ]

        try:
            subprocess.run(command, check=True)
            print(f"✅ 변환 완료! {self.converted_filename} 저장됨.")

            # ✅ 원본 파일 삭제
            os.remove(self.output_filename)
            os.remove(self.audio_filename)
            print(f"🗑️ 원본 파일 삭제 완료!")
        except subprocess.CalledProcessError as e:
            print(f"❌ 변환 실패: {e}")