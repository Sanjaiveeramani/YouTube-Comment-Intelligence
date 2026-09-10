import time
import pandas as pd

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import API_KEY


# Create YouTube API client
youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY,
    cache_discovery=False
)


def fetch_comments(video_id, max_comments=10000):

    comments = []
    comment_likes = []
    next_page_token = None

    print(f"Fetching comments for video: {video_id}")

    while len(comments) < max_comments:

        # Don't request more than 100 comments at once
        remaining = max_comments - len(comments)
        request_size = min(100, remaining)

        try:

            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=request_size,
                pageToken=next_page_token,
                textFormat="plainText"
            )

            # Retry up to 3 times if connection fails
            for attempt in range(3):

                try:
                    response = request.execute()
                    break

                except (ConnectionResetError, TimeoutError) as e:

                    print(
                        f"Connection error. "
                        f"Retry {attempt + 1}/3..."
                    )

                    if attempt == 2:
                        raise e

                    time.sleep(3)

        except HttpError as e:

            print("YouTube API error:")
            print(e)

            raise Exception(
                "YouTube API error. "
                "Check your API key, video ID, quota, "
                "or whether comments are enabled."
            )

        except Exception as e:

            print("Connection error:")
            print(e)

            raise Exception(
                "Could not connect to YouTube. "
                "Please check your internet connection and try again."
            )

        # -----------------------------------------
        # Extract comments
        # -----------------------------------------

        for item in response.get("items", []):

            try:

                top_level = item["snippet"]["topLevelComment"]["snippet"]

                comment = top_level["textDisplay"]
                likes = int(top_level.get("likeCount", 0))

                comments.append(comment)
                comment_likes.append(likes)

            except KeyError:
                continue

            if len(comments) >= max_comments:
                break

        # -----------------------------------------
        # Progress
        # -----------------------------------------

        print(
            f"Fetched {len(comments)} comments..."
        )

        # -----------------------------------------
        # Check next page
        # -----------------------------------------

        next_page_token = response.get(
            "nextPageToken"
        )

        if not next_page_token:
            print("No more comments available.")
            break

        # Small delay between requests
        time.sleep(0.5)

    # -----------------------------------------
    # Create DataFrame
    # -----------------------------------------

    df = pd.DataFrame({
        "Comment": comments,
        "Likes": comment_likes
    })

    # Save raw comments
    df.to_csv(
        "data/comments.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Finished! Total comments fetched: {len(df)}"
    )

    return df
