import random
import os

from moviepy import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip
)

GAMEPLAY_FOLDER = "gameplay"
VOICE_FILE = "output/voice.mp3"
OUTPUT_FILE = "output/short.mp4"


def generate_subtitles(script, duration):
    words = script.split()
    chunks = []
    
    # Using 1-2 words for high-speed 'viral' pacing
    temp = []
    for word in words:
        temp.append(word)
        if len(temp) == 2: # Keep it at 1 or 2 words max
            chunks.append(" ".join(temp))
            temp = []
    if temp:
        chunks.append(" ".join(temp))

    subtitles = []
    # Calculate duration per chunk
    chunk_duration = duration / len(chunks)

    for i, text in enumerate(chunks):
        txt = TextClip(
            text=text.upper(),
            font_size=110,           # Bigger font for 1-2 words
            color="white",
            stroke_color="black",
            stroke_width=3,
            method='caption',        # This is CRITICAL to keep text in bounds
            size=(900, None),        # Forces text to wrap if it hits 900px wide
            text_align='center'      # Centers the text inside that 900px box
        )

        # 960 is exact vertical center
        txt = txt.with_position(("center", 960))
        txt = txt.with_start(i * chunk_duration)
        txt = txt.with_duration(chunk_duration)

        subtitles.append(txt)

    return subtitles


def generate_video(script):

    videos = [f for f in os.listdir(GAMEPLAY_FOLDER) if f.endswith(".mp4")]

    random_video = random.choice(videos)
    video_path = os.path.join(GAMEPLAY_FOLDER, random_video)

    video = VideoFileClip(video_path)

    audio = AudioFileClip(VOICE_FILE)

    narration_duration = audio.duration
    video_duration = video.duration

    start_time = random.uniform(0, video_duration - narration_duration)
    end_time = start_time + narration_duration

    clip = video.subclipped(start_time, end_time)

    # convert to vertical
    clip = clip.resized(height=1920)

    clip = clip.cropped(
        x_center=clip.w / 2,
        width=1080,
        height=1920
    )

    # attach audio AFTER crop
    clip = clip.with_audio(audio)

    # now video is final 1080x1920
    subtitles = generate_subtitles(script, narration_duration)

    final_clip = CompositeVideoClip([clip, *subtitles], size=(1080, 1920))

    final_clip.write_videofile(
        OUTPUT_FILE,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        preset="ultrafast",
        threads=4
    )

    print("Short generated:", OUTPUT_FILE)