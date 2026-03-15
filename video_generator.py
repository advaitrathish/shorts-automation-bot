import random
import os

from moviepy import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    CompositeAudioClip
)

GAMEPLAY_FOLDER = "gameplay"
MUSIC_FOLDER = "music"

VOICE_FILE = "output/voice.mp3"
OUTPUT_FILE = "output/short.mp4"


# -----------------------------
# Subtitle Generator
# -----------------------------
def generate_subtitles(script, duration):

    words = script.split()

    subtitles = []

    word_duration = duration / len(words)

    # words that should stand out
    highlight_words = [
        "RUN",
        "DON'T",
        "STOP",
        "LOOK",
        "BEHIND",
        "WARNING",
        "DANGER",
        "HELP",
        "NOW",
        "CALL",
        "ANSWER",
        "WATCHING",
        "INSIDE"
    ]

    for i, word in enumerate(words):

        word_clean = word.upper().strip(".,!?")

        # highlight important words
        if word_clean in highlight_words:
            color = "red"
        else:
            color = "yellow"

        txt = TextClip(
            text=word.upper(),
            font_size=120,
            color=color,
            stroke_color="black",
            stroke_width=5,
            method="caption",
            size=(900, 320),
            text_align="center"
        ).with_position(("center",1500)) \
         .with_start(i * word_duration) \
         .with_duration(word_duration) \
         .resized(lambda t: 1 + 0.1 * t)

        subtitles.append(txt)

    return subtitles


# -----------------------------
# Random Background Music
# -----------------------------
def get_background_music(duration):

    if not os.path.exists(MUSIC_FOLDER):
        return None

    music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]

    if not music_files:
        return None

    music_path = os.path.join(MUSIC_FOLDER, random.choice(music_files))

    music = AudioFileClip(music_path)

    # loop or trim music to match narration
    if music.duration < duration:
        music = music.loop(duration=duration)
    else:
        music = music.subclipped(0, duration)

    # reduce music volume so narration stays clear
    music = music.with_volume_scaled(0.15)

    return music


# -----------------------------
# Main Video Generator
# -----------------------------
def generate_video(script):

    # load narration
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

    # -----------------------------
    # Background Music
    # -----------------------------
    music = get_background_music(narration_duration)

    if music:
        final_audio = CompositeAudioClip([audio, music])
    else:
        final_audio = audio

    clip = clip.with_audio(final_audio)

    # -----------------------------
    # Subtitles
    # -----------------------------
    subtitles = generate_subtitles(script, narration_duration)

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