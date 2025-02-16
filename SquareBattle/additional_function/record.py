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
        self.blackhole_device = self.get_blackhole_device()

    def get_blackhole_device(self):
        """ ✅ 정확한 'BlackHole 2ch' 오디오 장치를 자동으로 선택 """
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device["name"] == "BlackHole 2ch":  # ✅ 정확한 이름 매칭
                max_input_channels = device.get("max_input_channels", 0)  # ✅ 안전한 접근
                if max_input_channels > 0:
                    print(f"✅ 'BlackHole 2ch' 오디오 장치 선택: ID {i}")
                    return i
        print("❌ 'BlackHole 2ch' 오디오 장치를 찾을 수 없습니다.")
        return None

    def start_recording(self):
        """ 녹화 시작 (비디오 + 오디오) """
        print(f"🎥 녹화 시작! 파일 저장: {self.output_filename}")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(
            self.output_filename, fourcc, self.fps,
            (self.screen.get_width(), self.screen.get_height())
        )

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
        if self.blackhole_device is None:
            print("❌ 녹음을 진행할 수 없습니다. BlackHole 장치가 감지되지 않음.")
            return

        print("🎤 시스템 사운드 녹음 시작...")

        duration = 60  # ✅ 녹음 길이 (초)
        self.samplerate = 48000  # ✅ BlackHole 기본 샘플링 속도 적용
        self.channels = 2  # ✅ 스테레오 녹음

        # ✅ BlackHole을 통해 시스템 사운드 녹음
        audio_data = sd.rec(
            int(self.samplerate * duration),
            samplerate=self.samplerate,
            channels=self.channels,
            dtype="int16",
            device=self.blackhole_device
        )
        sd.wait()
        print("🎤 녹음 완료!")

        # ✅ 녹음된 데이터가 비어 있는지 확인
        if audio_data is None or np.all(audio_data == 0):
            print("⚠️ 녹음된 데이터가 없습니다. WAV 파일을 생성하지 않습니다.")
            return

        print(f"🎤 오디오 데이터 크기: {audio_data.shape}, 최대값: {np.max(audio_data)}, 최소값: {np.min(audio_data)}")

        # ✅ WAV 파일 저장
        sf.write(self.audio_filename, audio_data, self.samplerate)
        print(f"✅ 오디오 파일 저장 완료: {self.audio_filename}")
        print(f"🔍 저장된 오디오 파일 경로: {os.path.abspath(self.audio_filename)}")

    def merge_audio_video(self):
        """ 🎥 FFmpeg를 사용하여 비디오(`gameplay.mp4`)와 오디오(`audio.wav`)를 합쳐서 `gamePlayVideo` 디렉토리에 저장 """

        # ✅ 저장할 디렉토리 설정
        save_dir = "/Users/simjuheun/Desktop/개인프로젝트/MadeGame/SquareBattle/GamePlayRecord"
        os.makedirs(save_dir, exist_ok=True)  # ✅ 디렉토리가 없으면 자동 생성

        # ✅ 저장할 파일 경로
        output_path = os.path.join(save_dir, "gameplay_with_audio.mp4")

        if not os.path.exists("audio.wav"):
            print("❌ 오디오 파일이 존재하지 않습니다. 비디오만 저장됩니다.")
            return

        print(f"🔄 FFmpeg로 {output_path} 변환 중...")

        command = [
            "ffmpeg", "-i", "gameplay.mp4",  # ✅ 비디오 입력
            "-i", "audio.wav",  # ✅ 오디오 입력
            "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental",  # ✅ 비디오 & 오디오 설정
            output_path  # ✅ 저장할 위치 지정
        ]

        try:
            subprocess.run(command, check=True)
            print(f"✅ 변환 완료! 저장된 파일: {output_path}")

            # ✅ 원본 파일 삭제 (필요하면 주석 해제)
            os.remove("gameplay.mp4")
            os.remove("audio.wav")
            print(f"🗑️ 원본 파일 삭제 완료!")
        except subprocess.CalledProcessError as e:
            print(f"❌ 변환 실패: {e}")