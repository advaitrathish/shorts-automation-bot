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


# -----------------------------
# Subtitle Generator
# -----------------------------
def generate_subtitles(script, duration):

    words = script.split()

    subtitles = []

    word_duration = duration / len(words)

    for i, word in enumerate(words):

        # Highlight current word
        txt = TextClip(
            text=word.upper(),
            font_size=120,
            color="yellow",          # highlight color
            stroke_color="black",
            stroke_width=5,
            method="caption",
            size=(900, 320),
            text_align="center"
        )

        txt = TextClip(
            text=word.upper(),
            font_size=120,
            color="yellow",
            stroke_color="black",
            stroke_width=5,
            method="caption",
            size=(900, 320),
            text_align="center"
        ).with_position(("center",1500)).with_start(i * word_duration).with_duration(word_duration).resized(lambda t: 1 + 0.1 * t)

        subtitles.append(txt)

    return subtitles


# -----------------------------
# Main Video Generator
# -----------------------------
def generate_video(script):

    # load audio
    audio = AudioFileClip(VOICE_FILE)

    narration_duration = audio.duration

    # enforce minimum short length
    if narration_duration < 35:
        print("Narration too short, regenerating...")
        return None

    # get gameplay videos
    videos = [f for f in os.listdir(GAMEPLAY_FOLDER) if f.endswith(".mp4")]

    if not videos:
        raise Exception("No gameplay videos found in gameplay folder")

    random_video = random.choice(videos)

    video_path = os.path.join(GAMEPLAY_FOLDER, random_video)

    video = VideoFileClip(video_path)

    video_duration = video.duration

    # ensure gameplay is longer than narration
    if video_duration <= narration_duration:
        start_time = 0
    else:
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

    # attach narration
    clip = clip.with_audio(audio)

    # generate subtitles
    subtitles = generate_subtitles(script, narration_duration)

    # combine video + subtitles
    final_clip = CompositeVideoClip(
        [clip, *subtitles],
        size=(1080, 1920)
    )

    # export short
    final_clip.write_videofile(
        OUTPUT_FILE,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        preset="ultrafast",
        threads=4
    )

    print("Short generated:", OUTPUT_FILE)

    return OUTPUT_FILE