from script_generator import generate_script
from voice_generator import generate_voice
from video_generator import generate_video


def main():

    print("Generating script...")
    script = generate_script()

    print("\nSCRIPT:\n")
    print(script)

    print("\nGenerating voice...")
    generate_voice(script)

    print("Generating video...")
    generate_video(script)

    print("\nShort created successfully!")


if __name__ == "__main__":
    main()