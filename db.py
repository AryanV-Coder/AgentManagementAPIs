from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_DB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())

db = client.agents_db
collection = db['agents_data']
