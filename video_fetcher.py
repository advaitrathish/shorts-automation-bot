import requests
import random
import os

PEXELS_API_KEY = "B7lFhvbahwA84cBOoMPxa297o1vbJIo6xwDyHnBGjRxxxR6f7nRsUAZm"

headers = {
    "Authorization": PEXELS_API_KEY
}


def download_video(query, filename):

    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15"

    response = requests.get(url, headers=headers)
    data = response.json()

    videos = data.get("videos", [])

    if not videos:
        print("No videos found for:", query)
        return None

    video = random.choice(videos)
    video_files = video["video_files"]

    best_video = None

    for vf in video_files:
        width = vf.get("width", 0)
        height = vf.get("height", 0)

        if height > width:  # prefer vertical
            best_video = vf["link"]
            break

    if not best_video:
        best_video = video_files[0]["link"]

    video_data = requests.get(best_video).content

    path = f"assets/{filename}"

    with open(path, "wb") as f:
        f.write(video_data)

    print("Downloaded:", path)

    return path


def download_multiple_videos(script):

    words = script.lower().replace(".", "").replace(",", "").split()

    queries = list(set(words[:6]))

    clips = []

    os.makedirs("assets", exist_ok=True)

    for i, word in enumerate(queries[:4]):   # download 4 clips

        filename = f"clip_{i}.mp4"

        path = download_video(word, filename)

        if path:
            clips.append(path)

    return clips