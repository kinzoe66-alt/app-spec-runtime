import requests


def send_request(target: str):

    response = requests.get(
        target,
        timeout=5
    )

    return {
        "status_code": response.status_code,
        "url": response.url,
        "headers": dict(response.headers)
    }