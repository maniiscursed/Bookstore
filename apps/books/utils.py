import re

import requests


def download_image_bytes(url):
    try:
        response = requests.get(
            url,
            timeout=20,
            headers={'User-Agent': 'Mozilla/5.0'},
        )
        if response.status_code != 200:
            return None

        content = response.content
        content_type = (response.headers.get('content-type') or '').lower()

        if len(content) < 1000:
            return None

        if 'image' not in content_type and not content.startswith((b'\xff\xd8\xff', b'\x89PNG', b'GIF87a', b'GIF89a')):
            return None

        return content
    except requests.RequestException:
        return None


def extract_og_image(page_url):
    try:
        response = requests.get(
            page_url,
            timeout=20,
            headers={'User-Agent': 'Mozilla/5.0'},
        )
        if response.status_code != 200:
            return None

        html = response.text
        patterns = [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1)
        return None
    except requests.RequestException:
        return None


def download_cover_from_url(url):
    if not url:
        return None

    image_bytes = download_image_bytes(url)
    if image_bytes:
        return image_bytes

    og_image_url = extract_og_image(url)
    if og_image_url:
        return download_image_bytes(og_image_url)

    return None