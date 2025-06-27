from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
from dotenv import load_dotenv
import os

load_dotenv()

# Check if running in CI environment
is_ci = os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true'

if is_ci:
    # CI environment - use local MongoDB without SSL
    uri = "mongodb://localhost:27017"
    print("🔧 CI Environment detected - using local MongoDB")
    client = MongoClient(uri)
else:
    # Production/Local development - use MongoDB Atlas with SSL
    uri = os.getenv("MONGO_DB_URI")
    print("🌐 Production Environment - using MongoDB Atlas")
    if uri:
        client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    else:
        # Fallback to local MongoDB if no URI provided
        print("⚠️  No MONGO_DB_URI found, falling back to local MongoDB")
        uri = "mongodb://localhost:27017"
        client = MongoClient(uri)

db = client.agents_db
collection = db['agents_data']

print(f"📁 Connected to MongoDB: {uri.split('@')[-1] if '@' in uri else uri}")
