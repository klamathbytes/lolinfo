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

# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        ignore_tags = ["br", "a", "font"]
        if tag not in ignore_tags:
            print("Encountered a start tag:", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


string_jsonpy = {
    "#!/usr/bin/python3": {},
    "from sqlalchemy import Table, Column, MetaData, types, create_engine": {},
    "from sqlalchemy.ext.declarative import declarative_base": {},
    "from sqlalchemy.orm import sessionmaker": {},
    "import json": {},
    "base = declarative_base()": {},
    "class SQLTable(base):": {
        # ---- Data Rows that python will populate
        # ----
    },
    "def run():": {"return True": {},},
    "def DataBuilder(key,sql_row,data):": {},
    "def InitilizeBuilder(postgres_engine):": {
        "base.metadata.create_all(postgres_engine)": {},
        "sql_table = SQLTable()": {},
        "return sql_table": {},
    },
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
url_text = "https://ddragon.leagueoflegends.com/api/versions.json"


def get_api(url_text):
    url = urllib.request.urlopen(url_text)
    data = url.read()
    encoding = url.info().get_content_charset("utf-8")
    return json.loads(data.decode(encoding))


def get_unique_keys(unique_json, key, data):
    # print(unique_json, key, data)
    data_type = str(type(data[key]))
    # input("80")
    # if "description" in key:
    #     # input("stopper")
    #     print(data[key], data_type, isinstance(data[key], str), "</" in data[key])
    try:
        if (unique_json[key][data_type] or unique_json[key]["HTML"]) and data != {}:
            unique_json[key][data_type] += 1
            # print(unique_json, key, data)
            # input("85")
        elif isinstance(data[key], str) and "</" in data[key]:
            unique_json.update({f"{key}": {"HTML": 1}})
    except TypeError:
        # print(unique_json, key, data)
        # input("88")
        unique_json.update({f"{key}": {f"{data_type}": 1}})
    except KeyError:
        if isinstance(data[key], str) and "</" in data[key]:
            unique_json.update({f"{key}": {"HTML": 1}})
        else:
            unique_json[key] = {f"{data_type}": 1}
        # print(unique_json, key, data)
        # input("93")
    finally:
        # input("95")
        return unique_json


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
base = declarative_base()
databaseMetaData = MetaData(postgres_engine)
psql_session = (sessionmaker(postgres_engine))()
base.metadata.create_all(postgres_engine)
# runes, https://ddragon.leagueoflegends.com/cdn/10.11.1/data/en_US/runesReforged.json
version_data = ["10.11.1"]
for version in version_data:
    # try:
    #     champion_data = get_api(
    #         f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    #     )
    #     champion_data = json.loads(json.dumps(champion_data["data"]))
    #     # AllData[version] = champion_data
    #     for champion_id, data in champion_data.items():
    #         print(champion_id)
    #         champion_detail_data = get_api(
    #             f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion_id}.json"
    #         )
    # except Exception as e:
    #     print("Had error on version: {0} with error: {1}", version, e)

    try:
        itemData = get_api(
            f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
        )
        # this will be build/generated automatically in the future
        string_jsonpy["class SQLTable(base):"] = {
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
        # print(items)
        AllData[version] = items
        sqlRow = jsonpy.pywrite(string_jsonpy)
        for item, data in items.items():
            dynampySuccess = jsonpy.pywrite(string_jsonpy)
            for key in data.keys():
                # input("stoper 256")
                value = data[key]
                UniqueItemKeys = get_unique_keys(UniqueItemKeys, key, data)
                import dynampy

                # input("284")
                sqlRow = dynampy.InitilizeBuilder(postgres_engine)
                sqlRow = dynampy.DataBuilder(key, sqlRow, value)
                # jpy_SQL_params = jpy_SQL_params + f", {key} = {data_type}({value})"
            sqlRow.item_item = item
            sqlRow.item_version = version
            psql_session.add(sqlRow)
            psql_session.commit()
            # string_jsonpy["def run():"]["loaded_sql_row = SQLRow()"] = (
            #    jpy_SQL_params + ")"
            # )
        versions_count += 1

    except KeyError as e:
        print("Had error on version: {0} with error: {1}", version, e)
with open("item_data_types.json", "w", encoding="utf-8") as f:
    json.dump(UniqueItemKeys, f, ensure_ascii=False, indent=4)
print(UniqueItemKeys)
print(UniqueItemSqlTypes)
print(versions_count)
