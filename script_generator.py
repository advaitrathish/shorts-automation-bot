import requests
import random
import os

# GROQ API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Prevent duplicate stories during one run
generated_stories = set()


# -----------------------------
# THEMES (story direction)
# -----------------------------
themes = [

    "creepy phone message",
    "unknown caller horror",
    "haunted smartphone",
    "strange late night notification",
    "AI assistant behaving strangely",

    "phone receiving messages from the future",
    "a call from your own phone number",
    "phone camera turning on by itself",
    "phone showing a message before it happens",

    "smart home device acting possessed",
    "voice assistant whispering at night",
    "AI device predicting someone's death",

    "someone texting from inside the house",
    "receiving messages from a dead contact",
    "phone showing photos that were never taken",

    "phone unlocking itself at night",
    "strange countdown appearing on the phone",
    "phone warning about someone nearby",

    "unknown bluetooth device connecting",
    "phone recording without permission",
    "phone showing a live camera feed",

    "unknown person controlling your phone",
    "device showing your exact location",
    "message saying someone is watching you",

    "a phone notification predicting danger",
    "a mysterious message telling you to run",
    "a phone call from your future self",

    "phone showing a map of your house",
    "phone identifying someone in the dark",
    "phone detecting movement in empty rooms",

    "an AI assistant becoming self aware",
    "a phone warning that reality is a simulation"
]


# -----------------------------
# HOOKS (first line)
# -----------------------------
hooks = [

    "Never answer a call from your own number.",
    "If your phone shows this message, run.",
    "Something terrifying happened last night.",
    "This happened to someone online.",
    "I should not have answered that call.",
    "My phone did something impossible.",
    "The message appeared at exactly 3:17 AM.",
    "I thought it was just a glitch at first.",
    "My phone started recording by itself.",
    "The caller ID showed my own name."
]


# -----------------------------
# STORY STYLES
# -----------------------------
prompt_styles = [

    "Write the story like a creepy personal experience.",
    "Write the story like a scary internet mystery.",
    "Write the story like a horror narration.",
    "Write the story like someone explaining a strange event.",
    "Write the story like a dark urban legend."
]


# -----------------------------
# AI STORY GENERATOR
# -----------------------------
def generate_script():

    while True:

        theme = random.choice(themes)
        hook = random.choice(hooks)
        style = random.choice(prompt_styles)

        prompt = f"""
Start the story with this hook:
{hook}

Then continue a creepy horror story.

Theme: {theme}

{style}

Rules:
- 90 to 110 words
- simple English
- easy to understand
- short sentences
- suspenseful pacing
- dramatic twist ending
- each sentence on a new line
- do not repeat common horror phrases
"""

        headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(GROQ_URL, headers=headers, json=payload)
        data = response.json()

        script = data["choices"][0]["message"]["content"].strip()

        # --- CLEANUP AI OUTPUT ---
        script = script.replace("Here's the story:", "")
        script = script.replace("Here is the story:", "")
        script = script.replace("Story:", "")
        script = script.strip()
        script = script.replace("...", ".")
        script = script.replace("..", ".")

        if not script:
            print("Empty story generated, retrying...")
            return generate_script()

        # Avoid duplicate stories in one session
        if script not in generated_stories:
            generated_stories.add(script)

            print("\nGenerated Story:\n")
            print(script)
            print("\n-----------------------\n")

            return script