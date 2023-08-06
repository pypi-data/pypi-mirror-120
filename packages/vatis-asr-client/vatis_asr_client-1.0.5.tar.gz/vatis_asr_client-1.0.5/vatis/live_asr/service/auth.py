from vatis.live_asr.config_variables import API_KEY, AUTHENTICATION_PROVIDER_URL
import requests
from requests import Response


def get_auth_token() -> str:
    response: Response = requests.get(
        AUTHENTICATION_PROVIDER_URL,
        params={'service': 'LIVE_ASR'},
        headers={'Authorization': 'Bearer ' + API_KEY}
    )

    if response.status_code != 200:
        raise ConnectionAbortedError(f'Bad status code {response.status_code}')

    return response.text
