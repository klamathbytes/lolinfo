#!/usr/bin/python3
import urllib.request
import json
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        ignore_tags = ["br", "a", "font"]
        if tag not in ignore_tags:
            print("Encountered a start tag:", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


# API documents
# https://developer.riotgames.com/docs/lol#game-client-api_replay-api
# versions
url_text = f"https://ddragon.leagueoflegends.com/api/versions.json"


def get_api(url_text):
    url = urllib.request.urlopen(url_text)
    data = url.read()
    encoding = url.info().get_content_charset("utf-8")
    return json.loads(data.decode(encoding))


version_data = get_api(url_text)
versionX = ""
UniqueItemKeys = {}
AllData = {}
versions_count = 0
for version in version_data:
    try:
        # version: lolpatch_3.7 had an error
        itemData = get_api(
            f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
        )
        items = json.loads(json.dumps(itemData["data"]))
        AllData[version] = items
        for item, data in items.items():
            # print(item, data.keys())
            for key in data.keys():
                UniqueItemKeys[key] = 1
        versions_count += 1
    except Exception as e:
        print("Had error on version: {0} with error: {1}", version, e)
with open("item_data.json", "w", encoding="utf-8") as f:
    json.dump(AllData, f, ensure_ascii=False, indent=4)
print(UniqueItemKeys)
print(versions_count)


# print(data["name"])
# datat descpt isn't perfect needs work
# description = "<data>"+data["description"].replace("<br>",'')+"</data>"
# parser = MyHTMLParser()
# parser.feed(data["description"])
# print(data["description"])
# print(type(data["description"]),data["description"],"<data>"+data["description"]+"</data>")
# print(json.dumps(xmltodict.parse(description))) #json.dumps(xmltodict.parse(data["description"]))
# print(data["colloq"])
# print(data["plaintext"])
# needs a try catch for all of these
# print(data["into"])
# print(data["gold"])
# print(data["tags"])
# print(data["maps"])
# print(data["stats"])
# break
# break
# item data
# https://ddragon.leagueoflegends.com/cdn/9.8.1/data/en_US/item.json
# Champion data
# https://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion.json
# Champion Detailed Data
# https://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion/Aatrox.json
# riotAPIKey = os.environ['RIOT_API_KEY']
# url_text = f"https://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion.json"
# print(riotAPIKey)
