import asyncio
import logging
from datetime import datetime, timezone
from backend.config.settings import settings
from backend.core.database import connect_db, disconnect_db, get_collection, Collections
from backend.core.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

async def seed_data():
    logger.info("Initializing database connection...")
    await connect_db()
    
    users = get_collection(Collections.USERS)
    
    # Check if test student user exists
    email = "student@example.com"
    existing = await users.find_one({"email": email})
    if existing:
        logger.info(f"Test user {email} already exists.")
    else:
        logger.info(f"Seeding test student user: {email}")
        hashed = hash_password("Password123!")
        user_data = {
            "name": "Test Student",
            "email": email,
            "password_hash": hashed,
            "role": "student",
            "profile": {
                "skills": ["Python", "SQL", "Communication"],
                "gpa": 3.6,
                "internships": 1,
                "projects": 2,
            },
            "avatar": None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "is_active": True,
            "is_verified": True
        }
        await users.insert_one(user_data)
        logger.info("Test student seeded successfully.")

    # Check if admin user exists
    admin_email = "admin@example.com"
    existing_admin = await users.find_one({"email": admin_email})
    if existing_admin:
        logger.info(f"Admin user {admin_email} already exists.")
    else:
        logger.info(f"Seeding admin user: {admin_email}")
        hashed = hash_password("AdminPassword123!")
        admin_data = {
            "name": "Test Admin",
            "email": admin_email,
            "password_hash": hashed,
            "role": "admin",
            "profile": {},
            "avatar": None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "is_active": True,
            "is_verified": True
        }
        await users.insert_one(admin_data)
        logger.info("Admin user seeded successfully.")
        
    await disconnect_db()
    logger.info("Database seeding process finished.")

if __name__ == "__main__":
    asyncio.run(seed_data())
