import requests
import csv
import time

API_KEY = ''  # 🔑 Replace with your actual API key
SEARCH_QUERY = 'blockchain'  # 🔍 Change this to your topic of interest
MAX_RESULTS = 50  # Max allowed per page
video_data = []
next_page_token = ''
Relevance_Language = 'en'

print("🚀 Starting YouTube Data API scraping...")

while len(video_data) < 1000:
    search_url = (
        f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video'
        f'&q={SEARCH_QUERY}&maxResults={MAX_RESULTS}&relevanceLanguage={Relevance_Language}&key={API_KEY}&pageToken={next_page_token}'
    )
    search_response = requests.get(search_url).json()

    # ✅ Filter only video items safely
    video_ids = [
        item['id']['videoId']
        for item in search_response.get('items', [])
        if item.get('id', {}).get('kind') == 'youtube#video' and 'videoId' in item['id']
    ]

    if not video_ids:
        print("⚠️ No video IDs found on this page. Stopping.")
        break

    # 📊 Fetch video statistics
    stats_url = (
        f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics'
        f'&id={",".join(video_ids)}&key={API_KEY}'
    )
    stats_response = requests.get(stats_url).json()

    for item in stats_response.get('items', []):
        snippet = item.get('snippet', {})
        stats = item.get('statistics', {})
        video_data.append([
            snippet.get('channelTitle', 'N/A'),
            snippet.get('title', 'N/A'),
            stats.get('viewCount', 'N/A'),
            stats.get('likeCount', 'N/A'),
            stats.get('commentCount', 'N/A')
        ])

    print(f"✅ Fetched {len(video_data)} records so far...")

    next_page_token = search_response.get('nextPageToken', '')
    if not next_page_token:
        print("⛔ No more pages available.")
        break

    time.sleep(1)  # ⏱️ Respect API rate limits

# 💾 Save to CSV
with open("youtube_blockchain_records1.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Channel Name", "Video Title", "Views", "Likes", "Comments"])
    writer.writerows(video_data)

print("🎉 Done! Saved  records to youtube_blockchain_records1.csv")