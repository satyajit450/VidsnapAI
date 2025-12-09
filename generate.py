import os
import time,subprocess
from text_to_speech import text_to_speech_file

def text_to_audio(folder) :
    print("TTA:",folder)
    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()
    print(text, folder)
    text_to_speech_file(text,folder)

def create_reel(folder):
    os.makedirs("static/reels", exist_ok=True)

    command = (
    r'ffmpeg -f concat -safe 0 '
    rf'-i "C:\Users\satya\OneDrive\Documents\vidsnap\user_uploads\{folder}\input.txt" '
    rf'-i "C:\Users\satya\OneDrive\Documents\vidsnap\user_uploads\{folder}\output_reel_with_audio.mp3" '
    r'-vf "scale=1080:1920:force_original_aspect_ratio=decrease,'
    r'pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
    rf'-c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p '
    rf'"C:\Users\satya\OneDrive\Documents\vidsnap\static\reels\{folder}.mp4"'
)


    subprocess.run(command, shell=True, check=True)
    print("CR:", folder)

if __name__ == "__main__" :
    while True:
        print("Processing queue...")
        with open("done.txt","r") as f:
            done_folders = f.readlines()
        done_folders = [f.strip() for f in done_folders]
        folders = os.listdir("user_uploads")
        for folder in folders :
            if folder not in done_folders:
                text_to_audio(folder)
                create_reel(folder)
                with open("done.txt","a") as f:
                    f.write(folder + "\n")


        time.sleep(4)