from yt_playlist_randomizer.get_credentials import get_credentials
from yt_playlist_randomizer.save_videoIDs_to_file import main as save_ids
from yt_playlist_randomizer.remake_playlist import main as remake

TARGET_PLAYLIST_URL = "https://www.youtube.com/playlist?list....."      
NUMBER_OF_VIDEOS_TO_ADD = 100

def main():
    print("=== YouTube Playlist Randomizer ===")
    creds = get_credentials()
    save_ids()
    remake(TARGET_PLAYLIST_URL, NUMBER_OF_VIDEOS_TO_ADD)
    print("Finished!")

if __name__ == "__main__":
    main()

