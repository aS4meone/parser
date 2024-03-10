from os import getenv

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = getenv('TG_TOKEN')
TG_ID = int(getenv('TG_ID'))