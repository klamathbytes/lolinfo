#!/usr/bin/python3
import os
import urllib.request
import json
import xmltodict

#API documents
#https://developer.riotgames.com/docs/lol#game-client-api_replay-api
#versions
urlText = f"https://ddragon.leagueoflegends.com/api/versions.json"

def getApi(urlText):
    url = urllib.request.urlopen(urlText)
    data = url.read()
    encoding = url.info().get_content_charset('utf-8')
    return json.loads(data.decode(encoding))

versionData = getApi(urlText)
versionX =''
for version in versionData:
    print(version)
    #version: lolpatch_3.7 had an error
    itemData = getApi(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json")
    items = json.loads(json.dumps(itemData["data"]))
    for item,data in items.items():
        print(item)
        print(data["name"])
        #datat descpt isn't perfect needs work
        description = "<data>"+data["description"].replace("<br>",'')+"</data>"
        print(type(data["description"]),data["description"],"<data>"+data["description"]+"</data>")
        print(json.dumps(xmltodict.parse(description))) #json.dumps(xmltodict.parse(data["description"]))
        print(data["colloq"])
        print(data["plaintext"])
        #needs a try catch for all of these
        #print(data["into"])
        print(data["gold"])
        print(data["tags"])
        print(data["maps"])
        print(data["stats"])
        #break
    break
#item data
#https://ddragon.leagueoflegends.com/cdn/9.8.1/data/en_US/item.json
#Champion data
#https://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion.json
#Champion Detailed Data
#https://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion/Aatrox.json
#riotAPIKey = os.environ['RIOT_API_KEY']
#urlText = f"https://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion.json"
#print(riotAPIKey)
