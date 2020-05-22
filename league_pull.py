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
import configparser


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        ignore_tags = ["br", "a", "font"]
        if tag not in ignore_tags:
            print("Encountered a start tag:", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


string_jsonpy = {
    "from sqlalchemy import Table, Column, MetaData, types, create_engine": {},
    "from sqlalchemy.ext.declarative import declarative_base": {},
    "from sqlalchemy.orm import sessionmaker": {},
    "import json": {},
    "import configparser": {},
    "#-------": {},
    "config = configparser.ConfigParser()": {},
    "config.read('.env')": {},
    "pg_url = config['postgres']['PGURL']": {},
    "db_string = pg_url": {},
    "postgres_engine = create_engine(db_string)": {},
    "#-------": {},
    "base = declarative_base()": {},
    "base.metadata.create_all(postgres_engine)": {},
    "class SQLRow(base):": {
        # ---- Data Rows that python will populate
        # ----
    },
    "def run():": {
        # ----
        "loaded_sql_row = SQLRow()": {},
        # "loaded_sql_row = SQLRow(": ")",
        # ----
        "return loaded_sql_row": {},
    },
    "def DataBuilder(key,sql_row,data):": {},
}

#  = {
# 	"item_version": sql_row.item_version = data,
# sql_row = fillDataRow[key]
# return sql_row"

# print(string_jsonpy["def run():"]["loaded_sql_row = SQLRow("])


# jsonpy.pywrite(jsonpy_item)
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

config = configparser.ConfigParser()
config.read(".env")
pg_user = config["postgres"]["PGUSER"]
pg_password = config["postgres"]["PGPASSWORD"]
pg_database = config["postgres"]["PGDATABASE"]
db_string = f"postgresql://{pg_user}:{pg_password}@localhost/{pg_database}"
postgres_engine = create_engine(db_string)
databaseMetaData = MetaData(postgres_engine)
psql_session = (sessionmaker(postgres_engine))()


for version in version_data:
    try:
        itemData = get_api(
            f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
        )
        # this will be build/generated automatically in the future
        string_jsonpy["class SQLRow(base):"] = {
            "__tablename__ = 'items'": {},
            "data_id = Column(types.INTEGER, primary_key=True)": {},
            "item_version = Column(types.VARCHAR)": {},
            "item_item = Column(types.INTEGER)": {},
            "item_name = Column(types.VARCHAR)": {},
            "item_description = Column(types.VARCHAR)": {},
            "item_colloq = Column(types.VARCHAR)": {},
            "item_plaintext = Column(types.VARCHAR)": {},
            "item_into = Column(types.ARRAY(types.INTEGER))": {},
            "item_image = Column(types.JSON)": {},
            "item_gold = Column(types.JSON)": {},
            "item_tags = Column(types.ARRAY(types.VARCHAR))": {},
            "item_maps = Column(types.JSON)": {},
            "item_stats = Column(types.JSON)": {},
            "item_from = Column(types.ARRAY(types.INTEGER))": {},
            "item_depth = Column(types.INTEGER)": {},
            "item_effect = Column(types.JSON)": {},
            "item_hideFromAll = Column(types.BOOLEAN)": {},
            "item_stacks = Column(types.DECIMAL)": {},
            "item_consumed = Column(types.BOOLEAN)": {},
            "item_inStore = Column(types.BOOLEAN)": {},
            "item_consumeOnFull = Column(types.BOOLEAN)": {},
            "item_specialRecipe = Column(types.DECIMAL)": {},
            "item_requiredChampion = Column(types.VARCHAR)": {},
            "item_requiredAlly = Column(types.VARCHAR)": {},
            "item_group = Column(types.VARCHAR)": {},
            "item_altimages = Column(types.JSON)": {},
        }
        # this will be build/generated automatically in the future
        string_jsonpy["def DataBuilder(key,sql_row,data):"] = {
            "if not key:": {"return sql_row": {}},
            "elif key in 'item_version':": {
                "sql_row.item_version = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_item':": {
                "sql_row.item_item = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_name':": {
                "sql_row.item_name = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_description':": {
                "sql_row.item_description = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_colloq':": {
                "sql_row.item_colloq = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_plaintext':": {
                "sql_row.item_plaintext = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_into':": {
                "sql_row.item_into = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_image':": {
                "sql_row.item_image = json.dumps(data)": {},
                "return sql_row": {},
            },
            "elif key in 'item_gold':": {
                "sql_row.item_gold = json.dumps(data)": {},
                "return sql_row": {},
            },
            "elif key in 'item_tags':": {
                "sql_row.item_tags = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_maps':": {
                "sql_row.item_maps = json.dumps(data)": {},
                "return sql_row": {},
            },
            "elif key in 'item_stats':": {
                "sql_row.item_stats = json.dumps(data)": {},
                "return sql_row": {},
            },
            "elif key in 'item_from':": {
                "sql_row.item_from = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_depth':": {
                "sql_row.item_depth = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_effect':": {
                "sql_row.item_effect = json.dumps(data)": {},
                "return sql_row": {},
            },
            "elif key in 'item_hideFromAll':": {
                "sql_row.item_hideFromAll = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_stacks':": {
                "sql_row.item_stacks = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_consumed':": {
                "sql_row.item_consumed = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_inStore':": {
                "sql_row.item_inStore = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_consumeOnFull':": {
                "sql_row.item_consumeOnFull = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_specialRecipe':": {
                "sql_row.item_specialRecipe = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_requiredChampion':": {
                "sql_row.item_requiredChampion = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_requiredAlly':": {
                "sql_row.item_requiredAlly = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_group':": {
                "sql_row.item_group = data": {},
                "return sql_row": {},
            },
            "elif key in 'item_altimages':": {
                "sql_row.item_altimages = json.dumps(data)": {},
                "return sql_row": {},
            },
        }
        items = json.loads(json.dumps(itemData["data"]))
        AllData[version] = items
        sqlRow = jsonpy.pywrite(string_jsonpy)
        for item, data in items.items():
            sqlRow = jsonpy.pywrite(string_jsonpy)
            # jpy_SQL_params = f"loaded_sql_row = SQLRow(item = {item}"
            for key in data.keys():

                value = data[key]
                import dynampy

                sqlRow = dynampy.DataBuilder(key, sqlRow, value)
                # 2 Lines below, is to determine the keys and data types
                # UniqueItemKeys[key] = 1
                # UniqueItemSqlTypes[key] = type(data[key])
                data_type = type(data[key])
                # jpy_SQL_params = jpy_SQL_params + f", {key} = {data_type}({value})"
            psql_session.add(sqlRow)
            psql_session.commit()
            # string_jsonpy["def run():"]["loaded_sql_row = SQLRow()"] = (
            #    jpy_SQL_params + ")"
            # )
        versions_count += 1
    except Exception as e:
        print("Had error on version: {0} with error: {1}", version, e)
# with open("item_data.json", "w", encoding="utf-8") as f:
#     json.dump(AllData, f, ensure_ascii=False, indent=4)
print(UniqueItemKeys)
print(UniqueItemSqlTypes)
print(versions_count)
