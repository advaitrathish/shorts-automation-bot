import asyncio
import random
import edge_tts

voices = [
    "en-US-AriaNeural",     # best female narration
    "en-GB-RyanNeural",     # very natural male
]


async def generate_voice_async(script, index):

    VOICE_FILE = f"output/voice_{index}.mp3"

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

    return VOICE_FILE


def generate_voice(script, index=0):

    voice_file = asyncio.run(generate_voice_async(script, index))

    print("Voice generated:", voice_file)

    return voice_file