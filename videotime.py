import subprocess
import os

def get_video_duration(file_path):
    duration = 0.0
    
    try:
        ffprobe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        result = subprocess.check_output(ffprobe_cmd).decode('utf-8').strip()
        duration = float(result)
        
    except Exception as e:
        print(f"Error getting duration for file {file_path}: {e}")
    
    return duration

folder_path = './raw_videos_0830/val'
total_duration = 0.0

for file_name in os.listdir(folder_path):
    if file_name.endswith(('.mp4', '.avi', '.mkv')):
        file_path = os.path.join(folder_path, file_name)
        duration = get_video_duration(file_path)
        total_duration += duration

print("Total duration of videos in the folder: ", total_duration, "seconds")