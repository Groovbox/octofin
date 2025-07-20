import requests

def is_url_reachable(url:str, timeout=5) -> bool:
    """Checks if the given URL is reachable."""

    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        return response.status_code < 400
    except requests.RequestException:
        return False
