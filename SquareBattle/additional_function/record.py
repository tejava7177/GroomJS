import cv2
import pygame
import numpy as np
import pyaudio
import wave
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

        # ✅ 오디오 녹음 관련 설정
        self.audio_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100
        self.chunk = 1024
        self.audio_interface = pyaudio.PyAudio()

    def start_recording(self):
        """ 녹화 시작 (비디오 + 오디오) """
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(self.output_filename, fourcc, self.fps, (self.screen.get_width(), self.screen.get_height()))

        if not self.video_writer.isOpened():
            print("❌ 오류: 비디오 파일을 생성할 수 없습니다.")
            return

        self.recording = True
        print(f"🎥 녹화 시작! 파일 저장: {self.output_filename}")

        # ✅ 오디오 녹음 시작 (별도 스레드 실행)
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
        """ Pygame 내부 사운드를 녹음 """
        print("🎤 오디오 녹음 시작...")

        stream = self.audio_interface.open(format=self.audio_format,
                                           channels=self.channels,
                                           rate=self.rate,
                                           input=True,
                                           frames_per_buffer=self.chunk)

        frames = []
        while self.recording:
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)

        print("🎤 오디오 녹음 종료!")
        stream.stop_stream()
        stream.close()

        # ✅ WAV 파일로 저장
        with wave.open(self.audio_filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio_interface.get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))

        print(f"✅ 오디오 파일 저장 완료: {self.audio_filename}")

    def merge_audio_video(self):
        """ FFmpeg를 사용하여 비디오와 오디오를 합침 """
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