import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from config import CHANNEL_ID
import json
import os

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_uploads_playlist_id():
    # Disable OAuthlib's HTTPS verification when running locally
    # **DISABLE** in production
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "auth/youtube-api-creds.json"

    # get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file,
        scopes
    )

    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        credentials=credentials
    )

    request = youtube.channels().list(
        part="contentDetails",
        id=CHANNEL_ID
    )

    response = request.execute()

    content_details = response["items"][0]["contentDetails"]
    upload_playlist_id = content_details["relatedPlaylists"]["uploads"]

    return upload_playlist_id, youtube


def get_latest_videos():
    playlist_id, youtube = get_uploads_playlist_id()

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=10
    )

    response = request.execute()

    with open("res.json", "w") as f:
        f.write(json.dumps(response))


if __name__ == "__main__":
    get_latest_videos()
