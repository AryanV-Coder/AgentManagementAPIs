"""
Test configuration for MongoDB connections
"""
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi


def get_test_mongodb_client():
    """
    Get MongoDB client configured for testing environment
    """
    # Always use local MongoDB for tests
    uri = "mongodb://localhost:27017"
    return MongoClient(uri)


def get_mongodb_client():
    """
    Get MongoDB client based on environment
    """
    # Check if running in CI environment
    is_ci = os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true'
    
    if is_ci:
        # CI environment - use local MongoDB without SSL
        uri = "mongodb://localhost:27017"
        print("🔧 CI Environment detected - using local MongoDB")
        return MongoClient(uri)
    else:
        # Production/Local development - use MongoDB Atlas with SSL
        uri = os.getenv("MONGO_DB_URI")
        print("🌐 Production Environment - using MongoDB Atlas")
        if uri:
            return MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        else:
            # Fallback to local MongoDB if no URI provided
            print("⚠️  No MONGO_DB_URI found, falling back to local MongoDB")
            uri = "mongodb://localhost:27017"
            return MongoClient(uri)
