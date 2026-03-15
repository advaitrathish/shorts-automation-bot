from script_generator import generate_script
from voice_generator import generate_voice
from video_generator import generate_video
from youtube_uploader import upload_video


def main():

    print("Generating script...")
    script = generate_script()

    print("\nSCRIPT:\n")
    print(script)

    # Create multiple shorts from one script
    for i in range(3):

        print(f"\nGenerating short {i+1}")

        voice_file = generate_voice(script, index=i)

        video_file = generate_video(script, voice_file, index=i)

        upload_video(video_file)


if __name__ == "__main__":
    main()