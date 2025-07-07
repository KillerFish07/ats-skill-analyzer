import requests

API_KEY = "c572b8783da69288be9a083883acb06f6975f49a"
SERPER_URL = "https://google.serper.dev/search"

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def search_learning_links(skill, max_results=5):
    query = f"learn {skill} site:geeksforgeeks.org OR site:w3schools.com OR site:freecodecamp.org"
    data = { "q": query }

    response = requests.post(SERPER_URL, headers=headers, json=data)
    if response.status_code != 200:
        print(f"❌ Serper error ({response.status_code}) for {skill}")
        return []

    results = response.json().get("organic", [])[:max_results]
    resources = []
    for item in results:
        resources.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "source": item.get("link").split('/')[2],
            "free": True
        })

    return resources

def search_youtube_videos(skill, max_results=3):
    query = f"{skill} tutorial site:youtube.com"

    response = requests.post(
        "https://google.serper.dev/videos",
        headers=headers,
        json={"q": query}
    )

    if response.status_code != 200:
        print(f"❌ Error fetching videos for {skill}: {response.status_code}")
        return []

    results = response.json().get("videos", [])[:max_results]
    videos = []

    for vid in results:
        thumbnail = vid.get("thumbnailUrl") or ""
        videos.append({
            "title": vid.get("title"),
            "url": vid.get("link"),
            "thumbnail": thumbnail,
            "source": "YouTube",
            "free": True
        })

    return videos
