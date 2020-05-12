import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
