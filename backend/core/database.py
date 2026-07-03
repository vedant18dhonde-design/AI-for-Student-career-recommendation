"""MongoDB database connection and collection accessors using Motor (async driver)."""

import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, IndexModel

from backend.config.settings import settings

logger = logging.getLogger(__name__)

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


async def connect_db() -> None:
    """Connect to MongoDB Atlas."""
    global _client, _db
    try:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000,
            maxPoolSize=10,
            minPoolSize=2,
        )
        _db = _client[settings.MONGODB_DB_NAME]
        # Ping to verify connection
        await _client.admin.command("ping")
        logger.info("✅ Connected to MongoDB: %s", settings.MONGODB_DB_NAME)
        await _create_indexes()
    except Exception as exc:
        logger.error("❌ MongoDB connection failed: %s", exc)
        raise


async def disconnect_db() -> None:
    """Disconnect from MongoDB."""
    global _client
    if _client:
        _client.close()
        logger.info("🔌 MongoDB disconnected")


def get_database() -> AsyncIOMotorDatabase:
    """Return the active database instance."""
    if _db is None:
        raise RuntimeError("Database not connected. Call connect_db() first.")
    return _db


# ── Collection accessors ─────────────────────────────────────────────────────

def get_collection(name: str):
    return get_database()[name]


class Collections:
    USERS = "users"
    PREDICTIONS = "predictions"
    RESUMES = "resumes"
    NOTIFICATIONS = "notifications"
    FEEDBACK = "feedback"
    REFRESH_TOKENS = "refresh_tokens"
    RESET_TOKENS = "reset_tokens"
    ANALYTICS = "analytics"


# ── Index creation ────────────────────────────────────────────────────────────

async def _create_indexes() -> None:
    """Create MongoDB indexes for performance."""
    db = get_database()
    try:
        # Users
        await db[Collections.USERS].create_indexes([
            IndexModel([("email", ASCENDING)], unique=True),
            IndexModel([("role", ASCENDING)]),
            IndexModel([("created_at", ASCENDING)]),
        ])

        # Predictions
        await db[Collections.PREDICTIONS].create_indexes([
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("prediction_type", ASCENDING)]),
            IndexModel([("created_at", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), ("prediction_type", ASCENDING)]),
        ])

        # Notifications
        await db[Collections.NOTIFICATIONS].create_indexes([
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("is_read", ASCENDING)]),
        ])

        # Resumes
        await db[Collections.RESUMES].create_indexes([
            IndexModel([("user_id", ASCENDING)], unique=True),
        ])

        # Refresh tokens
        await db[Collections.REFRESH_TOKENS].create_indexes([
            IndexModel([("token", ASCENDING)], unique=True),
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0),
        ])

        # Reset tokens
        await db[Collections.RESET_TOKENS].create_indexes([
            IndexModel([("token", ASCENDING)], unique=True),
            IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0),
        ])

        logger.info("✅ MongoDB indexes created")
    except Exception as exc:
        logger.warning("⚠️ Index creation warning: %s", exc)
