import requests


def check_is_site_exist(url) -> bool:
    try:
        response = requests.head(url)
        return response.status_code == 200 or response.ok
    except requests.ConnectionError:
        return False
