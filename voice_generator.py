import asyncio
import random
import edge_tts

VOICE_FILE = "output/voice.mp3"

voices = [

    "en-US-GuyNeural",
    "en-US-AndrewNeural",

    "en-US-JennyNeural",
    "en-US-AriaNeural"
]


async def generate_voice_async(script):

    voice = random.choice(voices)

    print("Selected voice:", voice)

    communicate = edge_tts.Communicate(
        text=script,
        voice=voice,
        rate="-5%",      # slightly slower for drama
        pitch="+2Hz",    # FIXED (must be Hz)
        volume="+0%"
    )

    await communicate.save(VOICE_FILE)


def generate_voice(script):

    asyncio.run(generate_voice_async(script))

    print("Voice generated:", VOICE_FILE)