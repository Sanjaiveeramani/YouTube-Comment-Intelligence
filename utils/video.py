from urllib.parse import urlparse, parse_qs


def extract_video_id(url):
    try:
        parsed_url = urlparse(url)

        # Normal YouTube URL
        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            video_id = parse_qs(parsed_url.query).get("v")

            if video_id:
                return video_id[0]

        # Short YouTube URL
        if parsed_url.hostname == "youtu.be":
            return parsed_url.path.strip("/")

        return None

    except Exception:
        return None