#!/usr/bin/python3
import os
import urllib.request

#API documents
#https://developer.riotgames.com/docs/lol#game-client-api_replay-api
#versions
#https://ddragon.leagueoflegends.com/api/versions.json
#item data
#https://ddragon.leagueoflegends.com/cdn/9.8.1/data/en_US/item.json
#Champion data
#https://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion.json
#Champion Detailed Data
#https://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion/Aatrox.json
riotAPIKey = os.environ['RIOT_API_KEY']
urlText = f"https://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion.json"
print(riotAPIKey)
