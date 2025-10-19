# About

**YT Playlist Randomizer** is a Python tool that fetches one or more YouTube playlists, saves the IDs of videos within, and creates a new randomized playlist.
It uses the **YouTube Data API (v3)** and **Google OAuth 2.0** authentication.

---

## Requirements

- Python 3.10+
- A Google account with YouTube access
- A project set up in Google Cloud Console
- YouTube Data API v3 enabled
- `client_secret.json` file downloaded from Google Cloud (OAuth 2.0 credentials)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/alelys/YT_Playlist_Randomizer.git
   cd YT_Playlist_Randomizer
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate     # Linux / macOS
   venv\Scripts\activate        # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your `client_secret.json` file to the `data` folder.**

---

## OAuth Configuration and obtaining the `client_secret.json` file

1. Go to **Google Cloud Console → Credentials**
2. Click **Create Credentials → OAuth Client ID**
3. Choose **Desktop App** as the application type
4. Download the `.json` file (containing `client_id` and `client_secret`)
5. Rename it to `client_secret.json` and place it in the project directory
6. Add `http://localhost:8080/` to Authorized redirect URIs in your OAuth 2.0 Client options

When you run the program for the first time, it will open a browser window asking you to sign in to your Google account.
After authorization, it will generate a `token.json` file to store your credentials locally.

---

## Program configuration

1. **Edit main.py:**

- Set the target playlist (where randomized videos will be added):
  ```bash
  TARGET_PLAYLIST_URL = "https://www.youtube.com/playlist?list....."
  ```
- Set the number of videos you want to add:
  ```bash
  NUMBER_OF_VIDEOS_TO_ADD = 100
  ```

2. **Edit yt_playlist_randomizer\data\playlists_links.txt:**

- Add the links to playlists you want to randomize.
- Lines starting with # will be ignored (use this to comment out playlists).

  ```bash
  My Favorite Songs https://www.youtube.com/playlist?list=PLxxxxxx
  ```

---

## Running the Program

Run the main script:

    ```bash
    python main.py
    ```

---

# IMPORTANT

Before adding new videos, the script **removes all existing videos** from the target playlist (TARGET_PLAYLIST_URL).
Make sure you are using a dedicated empty playlist to avoid losing existing content.
