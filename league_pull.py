#!/usr/bin/python3
import urllib.request
import json
from html.parser import HTMLParser
from sqlalchemy import Table, Column, MetaData, types, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
import os
import jsonpy


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        ignore_tags = ["br", "a", "font"]
        if tag not in ignore_tags:
            print("Encountered a start tag:", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


pyjson = {
    "from sqlalchemy import Table, Column, MetaData, types, create_engine": {},
    "from sqlalchemy.ext.declarative import declarative_base": {},
    "from sqlalchemy.orm import sessionmaker": {},
    "base = declarative_base()": {},
    "class SQLRow(base):": {
        # ----
        "__tablename__ = 'items'": {},
        "data_id = Column(types.INTEGER, primary_key=True)": {},
        "item_id = Column(types.INTEGER)": {},
        "name = Column(types.VARCHAR)": {},
        # ----
    },
    "def run():": {
        # ----
        "loaded_sql_row = SQLRow(item_id=1,name=1)": {},
        # ----
        "return loaded_sql_row": {},
    },
}


# jsonpy.pywrite(pyjson_item)
# input("stopper")
# Need to loop thru and build dynamically the sql tables.
# Preferably loop only once over all the versions,
# and have the columns and data ready to be loaded into one table.
# If not loop twice... Or make tons of tables
# P-SUDO CODE for version item data loading to one table:
#


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
UniqueItemSqlTypes = {}
AllData = {}
versions_count = 0

for version in version_data:
    try:
        itemData = get_api(
            f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
        )
        pyjson["class SQLRow(base):"] = {
            "__tablename__ = items": {},
            "data_id = Column(types.INTEGER, primary_key=True)": {},
            "version = Column(types.VARCHAR)" "item = Column(types.INTEGER)": {},
            "name = Column(types.VARCHAR)": {},
            "description = Column(types.VARCHAR)": {},
            "colloq = Column(types.VARCHAR)": {},
            "plaintext = Column(types.VARCHAR)": {},
            "into = Column(types.ARRAY(types.INTEGER))": {},
            "image = Column(types.JSON)": {},
            "gold = Column(types.JSON)": {},
            "tags = Column(types.ARRAY(types.VARCHAR))": {},
            "maps = Column(types.JSON)": {},
            "stats = Column(types.JSON)": {},
            "from = Column(types.ARRAY(types.INTEGER))": {},
            "depth = Column(types.INTEGER)": {},
            "effect = Column(types.JSON)": {},
            "hideFromAll = Column(types.BOOL)": {},
            "stacks = Column(types.DECIMAL)": {},
            "consumed = Column(types.BOOL)": {},
            "inStore = Column(types.BOOL)": {},
            "consumeOnFull = Column(types.BOOL)": {},
            "specialRecipe = Column(types.DECIMAL)": {},
            "requiredChampion = Column(types.VARCHAR)": {},
            "requiredAlly = Column(types.VARCHAR)": {},
            "group = Column(types.VARCHAR)": {},
            "altimages = Column(types.VARCHAR)": {},
        }
        items = json.loads(json.dumps(itemData["data"]))
        AllData[version] = items
        for item, data in items.items():
            # print(item, data.keys())
            for key in data.keys():
                UniqueItemKeys[key] = 1
                UniqueItemSqlTypes[key] = type(data[key])

        versions_count += 1
    except Exception as e:
        print("Had error on version: {0} with error: {1}", version, e)
# with open("item_data.json", "w", encoding="utf-8") as f:
#     json.dump(AllData, f, ensure_ascii=False, indent=4)
print(UniqueItemKeys)
print(UniqueItemSqlTypes)
print(versions_count)
