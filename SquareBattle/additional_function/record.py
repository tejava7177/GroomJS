import cv2
import pygame
import numpy as np
import subprocess
import os

class GameRecorder:
    def __init__(self, screen, output_filename="gameplay.mp4", fps=30):
        """ 게임 화면을 녹화하는 클래스 """
        self.screen = screen
        self.fps = fps
        self.output_filename = output_filename
        self.converted_filename = "gameplay_converted.mp4"  # ✅ 변환된 파일명
        self.recording = False
        self.video_writer = None
        self.width, self.height = screen.get_size()

    def start_recording(self):
        """ 녹화 시작 """
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(self.output_filename, fourcc, self.fps, (self.width, self.height))
        self.recording = True
        print(f"🎥 녹화 시작! 파일 저장: {self.output_filename}")

    def capture_frame(self):
        """ 현재 Pygame 화면을 캡처하여 OpenCV 포맷으로 변환 후 저장 """
        if self.recording and self.video_writer and self.video_writer.isOpened():
            pygame_surface = pygame.display.get_surface()
            frame = pygame.surfarray.array3d(pygame_surface)

            if frame is None:  # ✅ 프레임이 None이면 저장하지 않음
                print("⚠️ 캡처된 프레임이 None입니다. 녹화를 중단합니다.")
                return

            frame = np.rot90(frame)  # OpenCV 형식으로 변환
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # 색상 변환
            self.video_writer.write(frame)

            print(f"✅ 프레임 저장됨 ({self.output_filename})")  # ✅ 로그 추가

    def stop_recording(self):
        """ 녹화 중지 및 저장 + FFmpeg 변환 """
        if self.recording:
            self.video_writer.release()
            self.recording = False
            print(f"🎬 녹화 완료! {self.output_filename} 저장됨.")

            # ✅ 녹화된 파일이 비어 있지 않은지 확인
            if os.path.exists(self.output_filename) and os.path.getsize(self.output_filename) > 0:
                self.convert_video()
            else:
                print("⚠️ 녹화된 파일이 비어 있습니다. 변환을 중단합니다.")

    def convert_video(self):
        """ FFmpeg를 사용하여 QuickTime 호환 MP4(H.264)로 변환 """
        print(f"🔄 FFmpeg로 {self.converted_filename} 변환 중...")

        command = [
            "ffmpeg", "-i", self.output_filename,
            "-vcodec", "libx264",  # ✅ H.264 코덱 사용
            "-an",  # ✅ 오디오 없이 변환 (FFmpeg 오류 방지)
            self.converted_filename
        ]

        try:
            subprocess.run(command, check=True)
            print(f"✅ 변환 완료! {self.converted_filename} 저장됨.")

            # ✅ 원본 파일 삭제 (필요 시 주석 처리 가능)
            os.remove(self.output_filename)
            print(f"🗑️ 원본 파일 {self.output_filename} 삭제됨.")
        except subprocess.CalledProcessError as e:
            print(f"❌ 변환 실패: {e}")