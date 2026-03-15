import asyncio
import random
import edge_tts

VOICE_FILE = "output/voice.mp3"

voices = [
    "en-US-AriaNeural",     # best female narration
    "en-GB-RyanNeural",     # very natural male
]


async def generate_voice_async(script):

    voice = random.choice(voices)

    print("Selected voice:", voice)

    # Add SSML formatting
    ssml_text = f"""
<speak>
<prosody rate="-5%" pitch="+2Hz">

{script.replace('.', '.<break time="300ms"/>')}

</prosody>
</speak>
"""

    communicate = edge_tts.Communicate(
        text=ssml_text,
        voice=voice
    )

    await communicate.save(VOICE_FILE)


def generate_voice(script):

    asyncio.run(generate_voice_async(script))

    print("Voice generated:", VOICE_FILE)