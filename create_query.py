from app import DB_CONNECTION_STRING

from sqlalchemy import create_engine
from sqlalchemy import sql

engine = create_engine(DB_CONNECTION_STRING)

query = ''
with open('./landmarks_by_proximity.sql', 'r') as f:
    query = f.read()

with engine.connect() as connection:
    connection.execute(sql.text(query))