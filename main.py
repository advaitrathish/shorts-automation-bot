from script_generator import generate_script
from voice_generator import generate_voice
from video_generator import generate_video

def main():

    while True:

        print("Generating script...")
        script = generate_script()

        print("\nSCRIPT:\n")
        print(script)

        print("\nGenerating voice...")
        generate_voice(script)

        print("Generating video...")
        result = generate_video(script)

        if result is not None:
            break

        print("Retrying generation...\n")


if __name__ == "__main__":
    main()