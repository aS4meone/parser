from os import getenv

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = getenv('TG_TOKEN')
TG_ID = int(getenv('TG_ID'))

DB_ENGINE = 'postgresql+psycopg2'
POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')
POSTGRES_HOST = getenv('POSTGRES_HOST')
POSTGRES_PORT = getenv('POSTGRES_PORT')

DATABASE_URL = (
    f"{DB_ENGINE}://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)