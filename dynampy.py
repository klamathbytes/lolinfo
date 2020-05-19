
from sqlalchemy import Table, Column, MetaData, types, create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
base = declarative_base() 
class LolItemSQLRow(base): 
	__tablename__ = "items" 
	data_id = Column(types.INTEGER, primary_key=True) 
	item_id = Column(types.INTEGER) 
	name = Column(types.VARCHAR) 

def run(): 
	loaded_sql_row = LolItemSQLRow(item_id=1,name=1) 
	return loaded_sql_row 

