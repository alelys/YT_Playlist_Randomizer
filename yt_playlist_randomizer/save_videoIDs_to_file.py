from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
PLAYLISTS_FILE = BASE_DIR / "data" / "playlists_links.txt"
OUTPUT_FILE = BASE_DIR / "data" / "video_IDs.txt"
TOKEN_FILE = BASE_DIR / "data" / "token.json"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def load_credentials():
    """Loads the credentials saved after authorization."""
    if not TOKEN_FILE.exists():
        raise FileNotFoundError("Missing token.json file, please run get_credentials.py first.")
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, ["https://www.googleapis.com/auth/youtube"])
    return creds


def read_playlists_from_file():
    """Loads playlists from the file, skipping comments and empty lines."""
    playlists = []

    if not os.path.exists(PLAYLISTS_FILE):
        print(f"File {PLAYLISTS_FILE} does not exist.")
        return playlists

    with open(PLAYLISTS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "playlist?list=" in line:
                playlist_id = line.split("playlist?list=")[1].strip()
                playlists.append(playlist_id)

    return playlists


def get_videos_from_playlist(youtube, playlist_id):
    """Returns a list of all video IDs from the given playlist."""
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids


def save_video_ids_to_file(video_ids):
    """Saves video IDs to a text file."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for vid in video_ids:
            file.write(f"{vid}\n")
    print(f"Saved {len(video_ids)} video IDs to file: {OUTPUT_FILE.name}")


def main():
    creds = load_credentials()
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    playlists = read_playlists_from_file()
    if not playlists:
        print("No playlists to process.")
        return

    all_video_ids = []
    for playlist_id in playlists:
        videos = get_videos_from_playlist(youtube, playlist_id)
        all_video_ids.extend(videos)
        print(f"Saved {len(videos)} videos from playlist: {playlist_id}")

    save_video_ids_to_file(all_video_ids)
    print("Finished!")


if __name__ == "__main__":
    main()
