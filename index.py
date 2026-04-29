import cv2
import os
import time
import numpy as np

def convert_frame_to_ascii(frame, width=150):
    """
    Convert a frame to ASCII art using a character set based on brightness
    """
    ascii_chars = " .:-=+*#%@"
    
    height = int(frame.shape[0] * width / frame.shape[1] / 2)
    if height == 0:
        height = 1
        
    resized_frame = cv2.resize(frame, (width, height))

    if len(resized_frame.shape) > 2:
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    else:
        gray_frame = resized_frame
    
    normalized = gray_frame / 255.0
    ascii_frame = ""
    
    # Fixed loop for explicit indexing
    for i in range(normalized.shape[0]):
        for j in range(normalized.shape[1]):
            pixel = normalized[i, j]
            index = int(pixel * (len(ascii_chars) - 1))
            ascii_frame += ascii_chars[index]
        ascii_frame += "\n"
    
    return ascii_frame

def play_video_in_terminal(video_path, width=150, fps=60):
    """
    Play a video in the terminal using ASCII characters
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    
    cap = cv2.VideoCapture(video_path)

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1.0 / video_fps if video_fps > 0 else 1.0 / fps
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            ascii_art = convert_frame_to_ascii(frame, width)
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)
            
            time.sleep(frame_delay)
            
    except KeyboardInterrupt:
        print("\nVideo playback interrupted.")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Default to local video.mp4
    default_video = "video.mp4"
    video_path = input(f"Enter the path to the video file (default: {default_video}): ").strip()
    if not video_path:
        video_path = default_video
    

    try:
        width = int(input("Enter width (default: 150): ") or "150")
    except ValueError:
        width = 150

    try:
        fps = int(input("Enter FPS (default: 60): ") or "60")
    except ValueError:
        fps = 60
    
    play_video_in_terminal(video_path, width, fps)

