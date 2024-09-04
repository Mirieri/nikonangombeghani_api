from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from . import models, schemas
from passlib.context import CryptContext
from typing import Optional, List
import logging
from fastapi import HTTPException

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def get_object_by_field(db: AsyncSession, model, field_name: str, field_value) -> Optional[object]:
    """Fetch a single object by a specified field."""
    try:
        result = await db.execute(select(model).filter(getattr(model, field_name) == field_value))
        return result.scalars().first()
    except Exception as e:
        logger.error(f"Error fetching {model.__name__} by {field_name}: {e}")
        return None


async def create_object(db: AsyncSession, model, obj_data: dict) -> Optional[object]:
    """Create a new object and save it to the database."""
    try:
        db_obj = model(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except IntegrityError as ie:
        logger.error(f"Integrity error while creating {model.__name__}: {ie}")
        raise HTTPException(status_code=400, detail="Integrity error, possibly due to duplicate entries.")
    except Exception as e:
        logger.error(f"Error creating {model.__name__}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the object.")


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> schemas.User:
    # Check if a user with the same username or email already exists
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail=f"User with username '{user.username}' already exists")

    existing_email = await get_object_by_field(db, models.User, 'email', user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail=f"User with email '{user.email}' already exists")

    # Prepare user data
    password_hash = pwd_context.hash(user.password)
    user_data = user.model_dump()

    # Convert role to enum
    try:
        user_role = models.UserRole[user.role] if isinstance(user.role, str) else user.role
        user_data['role'] = user_role.value
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid role: {user.role}")

    user_data['password_hash'] = password_hash
    user_data.pop('password')  # Remove plaintext password

    # Create and return the user object
    created_user = await create_object(db, models.User, user_data)

    if created_user is None:
        raise HTTPException(status_code=400, detail="User could not be created due to a database error")

    return schemas.User.model_validate(created_user)  # Ensure to convert to schema model


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[models.User]:
    return await get_object_by_field(db, models.User, 'user_id', user_id)


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.User]:
    return await get_object_by_field(db, models.User, 'username', username)

async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate) -> Optional[schemas.User]:
    """Update an existing user."""
    async with db.begin():
        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user_update.model_dump()

        if 'password' in user_data:
            user_data['password_hash'] = pwd_context.hash(user_data.pop('password'))

        try:
            for field, value in user_data.items():
                setattr(user, field, value)

            db.add(user)
            await db.commit()
            await db.refresh(user)
            return schemas.User.model_validate(user)
        except IntegrityError as ie:
            logger.error(f"Integrity error while updating user {user_id}: {ie}")
            raise HTTPException(status_code=400, detail="Integrity error, possibly due to duplicate entries.")
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while updating the user.")

async def delete_user(db: AsyncSession, user_id: int) -> Optional[schemas.User]:
    """Delete an existing user."""
    async with db.begin():
        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            await db.execute(delete(models.User).where(models.User.user_id == user_id))
            await db.commit()
            return schemas.User.model_validate(user)
        except IntegrityError as ie:
            logger.error(f"Integrity error while deleting user {user_id}: {ie}")
            await db.rollback()
            raise HTTPException(status_code=400, detail="Integrity error, possibly due to foreign key constraints.")
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            await db.rollback()
            raise HTTPException(status_code=500, detail="An error occurred while deleting the user.")

# Other CRUD functions remain unchanged...
