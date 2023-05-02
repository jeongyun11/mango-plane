import requests

def get_tour_data(api_key):
    url = "https://api.tourapi.com/tour/v1/lists"
    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data