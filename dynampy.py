
#!/usr/bin/python3 
from sqlalchemy import Table, Column, MetaData, types, create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
import json 
base = declarative_base() 
class SQLTable(base): 
	__tablename__ = "items" 
	data_id = Column(types.INTEGER, primary_key=True) 
	item_version = Column(types.VARCHAR) 
	item_item = Column(types.INTEGER) 
	item_name = Column(types.VARCHAR) 
	item_description = Column(types.VARCHAR) 
	item_colloq = Column(types.VARCHAR) 
	item_plaintext = Column(types.VARCHAR) 
	item_into = Column(types.ARRAY(types.INTEGER)) 
	item_image = Column(types.JSON) 
	item_gold = Column(types.JSON) 
	item_tags = Column(types.ARRAY(types.VARCHAR)) 
	item_maps = Column(types.JSON) 
	item_stats = Column(types.JSON) 
	item_from = Column(types.ARRAY(types.INTEGER)) 
	item_depth = Column(types.INTEGER) 
	item_effect = Column(types.JSON) 
	item_hideFromAll = Column(types.BOOLEAN) 
	item_stacks = Column(types.DECIMAL) 
	item_consumed = Column(types.BOOLEAN) 
	item_inStore = Column(types.BOOLEAN) 
	item_consumeOnFull = Column(types.BOOLEAN) 
	item_specialRecipe = Column(types.DECIMAL) 
	item_requiredChampion = Column(types.VARCHAR) 
	item_requiredAlly = Column(types.VARCHAR) 
	item_group = Column(types.VARCHAR) 
	item_altimages = Column(types.JSON) 

def run(): 
	return True 

def DataBuilder(key,sql_row,data): 
	if not key: 
		return sql_row 
	
	elif key in "item_version": 
		sql_row.item_version = data 
		return sql_row 
	
	elif key in "item_item": 
		sql_row.item_item = data 
		return sql_row 
	
	elif key in "item_name": 
		sql_row.item_name = data 
		return sql_row 
	
	elif key in "item_description": 
		sql_row.item_description = data 
		return sql_row 
	
	elif key in "item_colloq": 
		sql_row.item_colloq = data 
		return sql_row 
	
	elif key in "item_plaintext": 
		sql_row.item_plaintext = data 
		return sql_row 
	
	elif key in "item_into": 
		sql_row.item_into = data 
		return sql_row 
	
	elif key in "item_image": 
		sql_row.item_image = json.dumps(data) 
		return sql_row 
	
	elif key in "item_gold": 
		sql_row.item_gold = json.dumps(data) 
		return sql_row 
	
	elif key in "item_tags": 
		sql_row.item_tags = data 
		return sql_row 
	
	elif key in "item_maps": 
		sql_row.item_maps = json.dumps(data) 
		return sql_row 
	
	elif key in "item_stats": 
		sql_row.item_stats = json.dumps(data) 
		return sql_row 
	
	elif key in "item_from": 
		sql_row.item_from = data 
		return sql_row 
	
	elif key in "item_depth": 
		sql_row.item_depth = data 
		return sql_row 
	
	elif key in "item_effect": 
		sql_row.item_effect = json.dumps(data) 
		return sql_row 
	
	elif key in "item_hideFromAll": 
		sql_row.item_hideFromAll = data 
		return sql_row 
	
	elif key in "item_stacks": 
		sql_row.item_stacks = data 
		return sql_row 
	
	elif key in "item_consumed": 
		sql_row.item_consumed = data 
		return sql_row 
	
	elif key in "item_inStore": 
		sql_row.item_inStore = data 
		return sql_row 
	
	elif key in "item_consumeOnFull": 
		sql_row.item_consumeOnFull = data 
		return sql_row 
	
	elif key in "item_specialRecipe": 
		sql_row.item_specialRecipe = data 
		return sql_row 
	
	elif key in "item_requiredChampion": 
		sql_row.item_requiredChampion = data 
		return sql_row 
	
	elif key in "item_requiredAlly": 
		sql_row.item_requiredAlly = data 
		return sql_row 
	
	elif key in "item_group": 
		sql_row.item_group = data 
		return sql_row 
	
	elif key in "item_altimages": 
		sql_row.item_altimages = json.dumps(data) 
		return sql_row 
	

def InitilizeBuilder(postgres_engine): 
	base.metadata.create_all(postgres_engine) 
	sql_table = SQLTable() 
	return sql_table 

