import requests
import json

def call_AudD(sUrl):
    data = {
        "url": sUrl,
        "return": "spotify",
        "api_token": "Replace with your token."
    }
    result = requests.post("https://api.audd.io/", data=data)
    r = json.loads(result.text)
    if(result.status_code == requests.codes.ok):
        artist = r["result"]["artist"]
        title = r["result"]["title"]
        album = r["result"]["album"]
        songUrl = r["result"]["spotify"]["external_urls"]["spotify"]
        artistUrl = r["result"]["spotify"]["album"]["artists"][0]["external_urls"]["spotify"]
        imageLink = r["result"]["spotify"]["album"]["images"][0]["url"]
    arrAll = [artist, title, album, songUrl, artistUrl, imageLink]
    print(title)
    return arrAll
