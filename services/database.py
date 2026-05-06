"""
MongoDB Atlas connection manager.
Provides a singleton client and easy access to collections.
"""
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError

logger = logging.getLogger(__name__)

# Module-level singleton
_client = None
_db = None


def init_db(mongo_uri: str, db_name: str):
    """
    Initialize the MongoDB connection.
    Called once at app startup.
    """
    global _client, _db

    if not mongo_uri:
        logger.warning("MONGO_URI is empty — database features will be disabled.")
        return False

    try:
        _client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=20000,
            connectTimeoutMS=20000,
            socketTimeoutMS=20000,
            maxPoolSize=10
        )
        # Verify connection is alive
        _client.admin.command("ping")
        _db = _client[db_name]

        # Create indexes for performance
        _db.analyses.create_index("created_at")
        _db.analyses.create_index("filename")

        logger.info(f"✅ MongoDB connected successfully to database: {db_name}")
        return True

    except (ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError) as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        _client = None
        _db = None
        return False


def get_db():
    """Return the database instance, or None if not connected."""
    return _db


def get_collection(name: str):
    """Return a specific collection, or None if not connected."""
    if _db is None:
        return None
    return _db[name]


def is_connected() -> bool:
    """Check if the database is connected and responsive."""
    if _client is None:
        return False
    try:
        _client.admin.command("ping")
        return True
    except Exception:
        return False


def close_db():
    """Gracefully close the MongoDB connection."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB connection closed.")
