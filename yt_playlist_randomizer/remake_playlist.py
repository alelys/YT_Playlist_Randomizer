from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from pathlib import Path
import random
import time

BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "data" / "token.json"
VIDEO_IDS_FILE = BASE_DIR / "data" / "video_IDs.txt"
SCOPES = ["https://www.googleapis.com/auth/youtube"]

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def load_credentials():
    """Loads the credentials saved after authorization."""
    if not TOKEN_FILE.exists():
        raise FileNotFoundError("Missing token.json file – please run get_credentials.py first.")
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    return creds


def clear_playlist(youtube, playlist_id):
    """Removes all videos from the specified playlist."""
    total_deleted = 0
    next_page_token = None

    print(f"Removing videos from playlist {playlist_id}...")

    while True:
        request = youtube.playlistItems().list(
            part="id",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        items = response.get("items", [])
        if not items:
            break

        for item in items:
            playlist_item_id = item["id"]
            youtube.playlistItems().delete(id=playlist_item_id).execute()
            total_deleted += 1
            print(f"Removed {total_deleted}...")

            time.sleep(0.2)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    print(f"Removed a total of {total_deleted} videos.")


def load_video_ids():
    """Loads video IDs from the video_IDs.txt file."""
    if not VIDEO_IDS_FILE.exists():
        raise FileNotFoundError(f"Missing file {VIDEO_IDS_FILE.name}")
    with open(VIDEO_IDS_FILE, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def add_videos_to_playlist(youtube, playlist_id, video_ids, num_vids):
    """Adds new videos to the playlist."""
    print(f"Adding {num_vids} videos to the playlist {playlist_id}...")
    total_added = 0

    if num_vids > len(video_ids):
        num_vids = len(video_ids)
        print(f'Number of videos reduced to {num_vids}')

    random_vids = random.sample(video_ids, num_vids)

    for video_id in random_vids:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        try:
            request.execute()
            total_added += 1
            print(f"Added {total_added}/{num_vids}: {video_id}")
            time.sleep(0.2)  
        except:
            print(f"An issue occurred with {video_id}")

    print(f"Added {total_added} videos")


def main(url, num_vids):
    creds = load_credentials()
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    if "playlist?list=" not in url:
        print("Playlist link is invalid")
        return

    playlist_id = url.split("playlist?list=")[1]
    clear_playlist(youtube, playlist_id)

    video_ids = load_video_ids()
    add_videos_to_playlist(youtube, playlist_id, video_ids, num_vids)

    print("Playlist remake completed!")


if __name__ == "__main__":
    main()
