import requests
from config_data.config import RAPID_API_KEY
from aiogram.types import Message

url = "https://seeking-alpha.p.rapidapi.com"

querystring = {}

headers = {
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
}


def request(method: str, url: str, querystring: dict) -> requests.Response:
    """
        Посылаем запрос к серверу
        : param url : str
        : param query_string : dict
        : return : request.Response
    """

    if method == "GET":
        response_get = requests.get(url, headers=headers, params=querystring)
        return response_get
    elif method == "POST":
        response_post = requests.post(url, headers=headers, json=querystring)
        return response_post


def request_for_profile(method: str, query: dict) -> requests.Response:
    """
            Посылаем запрос к серверу для вытягивания профиля
            : param url : str
            : param query_string : dict
            : return : request.Response
        """

    if method == "GET":
        response_get = requests.get("https://seeking-alpha.p.rapidapi.com/symbols/get-profile", headers=headers,
                                    params=query)
        return response_get
    elif method == "POST":
        response_post = requests.post("https://seeking-alpha.p.rapidapi.com/symbols/get-profile", headers=headers,
                                      json=query)
        return response_post


async def auto_complete_func(message: Message):
    res_req = request("GET", "https://seeking-alpha.p.rapidapi.com/v2/auto-complete",
                          querystring={"query": message.text, 'type': 'symbols', 'size': 10})

    return res_req
