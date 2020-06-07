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
from collections import defaultdict

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
    data_type = str(type(data[key]))
    try:
        if (
            isinstance(data[key], str)
            and "</" in data[key]
            and not unique_json[key]["HTML"]
        ):
            unique_json.update({f"{key}": {"HTML": 1}})
        elif (unique_json[key][data_type] or unique_json[key]["HTML"]) and data != {}:
            unique_json[key][data_type] += 1
    except TypeError:
        unique_json.update({f"{key}": {f"{data_type}": 1}})
    except KeyError:
        if isinstance(data[key], str) and "</" in data[key]:
            unique_json.update({f"{key}": {"HTML": 1}})
        else:
            unique_json[key] = {f"{data_type}": 1}
    finally:
        return unique_json


# re-name this function to be the get all data and load or something
# for it pulls all the data and columns, and it would be easier to just load the data
# since all the columns we know the data structure
def get_defined_columns(model, versions_list, suffix_api_url):
    all_data = {}
    defined_columns = {}
    for version in version_data:
        try:
            data = get_api(
                f"https://ddragon.leagueoflegends.com/cdn/{version}/{suffix_api_url}"
            )
            data = json.loads(json.dumps(data["data"]))
            all_data[version] = data
            for league_object, object_data in data.items():
                for key in object_data.keys():
                    defined_columns = get_unique_keys(defined_columns, key, object_data)
        except urllib.error.HTTPError as e:
            print("Had error on version: {0} with error: {1}", version, e)

    for column, data_types in defined_columns.items():
        data_types_translator = {
            "<class 'str'>": {f"{model}_{column} = Column(types.VARCHAR)": {}},
            "<class 'NoneType'>": {f"{model}_{column} = Column(types.VARCHAR)": {}},
            # Would be nice to check VARCHAR or INTEGER
            "<class 'list'>": {
                f"{model}_{column} = Column(types.ARRAY(types.VARCHAR))": {}
            },
            "<class 'dict'>": {f"{model}_{column} = Column(types.JSON)": {}},
            "<class 'float'>": {f"{model}_{column} = Column(types.DECIMAL)": {}},
            "<class 'bool'>": {f"{model}_{column} = Column(types.BOOLEAN)": {}},
            # Need to break out the HTML tags and pull data from it?
            "HTML": {f"{model}_{column} = Column(types.VARCHAR)": {}},
            "<class 'int'>": {f"{model}_{column} = Column(types.INTEGER)": {}},
        }
        value_sectors = defaultdict(lambda: "data")
        value_sectors["<class 'dict'>"] = "json.dumps(data)"
        string_jsonpy["class SQLTable(base):"].update(
            {
                f"__tablename__ = '{model}'": {},
                "data_id = Column(types.INTEGER, primary_key=True)": {},
                f"{model}_version = Column(types.VARCHAR)": {},
                # Below would only work for the "item" model
                f"{model}_item = Column(types.INTEGER)": {},
            }
        )
        string_jsonpy["def DataBuilder(key,sql_row,data):"].update(
            {"if not key:": {"return sql_row": {}},}
        )
        for atype, occurances in data_types.items():
            string_jsonpy["class SQLTable(base):"].update(data_types_translator[atype])
            value = value_sectors[atype]
            string_jsonpy["def DataBuilder(key,sql_row,data):"].update(
                {
                    f"elif key in '{model}_{column}':": {
                        f"sql_row.{model}_{column} = {value}": {},
                        "return sql_row": {},
                    }
                },
            )

    json.dumps(defined_columns)
    print(json.dumps(string_jsonpy))


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
# version_data = ["10.11.1"]
sql_rows_collection = []

# Test was successful of "get_defined_columns"
# ------------------------------
test = get_defined_columns("item", version_data, "data/en_US/item.json")
input("stopper")
# ------------------------------
###############################
for version in version_data:
    try:
        champion_data = get_api(
            f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
        )
        champion_data = json.loads(json.dumps(champion_data["data"]))
        # AllData[version] = champion_data
        for champion_id, data in champion_data.items():
            print(champion_id)
            champion_detail_data = get_api(
                f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion_id}.json"
            )
    except Exception as e:
        print("Had error on version: {0} with error: {1}", version, e)

    try:
        itemData = get_api(
            f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
        )
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
