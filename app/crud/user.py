import logging

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import delete
from app import models
from app.models import User
from app.models.database import get_db, Base
from app.schema import schemas
from passlib.context import CryptContext
from typing import Optional, List
from fastapi import HTTPException, Depends, status
from typing import Type, Dict, Any

from app.schema.schemas import UserResponse
from app.utills.TransactionManager import TransactionManager

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


async def create_object(db: AsyncSession, model: Type[Base], obj_data: Dict[str, Any]) -> Any:
    try:
        db_obj = model(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError as e:
        logger.error("Database error occurred during object creation: %s", str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed.")
    except Exception as e:
        logger.error("Unexpected error occurred during object creation: %s", str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)) -> schemas.UserResponse:
    async with TransactionManager(db) as transaction:

        # Check if the user already exists
        result = await transaction.execute(select(User).filter(User.email == user.email))
        db_user = result.scalars().first()

        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        # Hash the password
        password_hash = pwd_context.hash(user.password)
        # Convert role from str to UserRole enum if necessary
        try:
            user_role = models.UserRole[user.role] if isinstance(user.role, str) else user.role
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid role: {user.role}")

        # Create the user object in the database
        db_user = User(
            username=user.username,
            email=user.email,
            role=user_role,
            phone=user.phone,
            address=user.address,
            password_hash=password_hash,
            last_login=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            status=models.user.UserStatus.Active
        )

        # Add the new user to the session
        transaction.add(db_user)
        await transaction.commit()
        await transaction.refresh(db_user)

    return UserResponse.from_orm(db_user)


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[models.User]:
    return await get_object_by_field(db, models.User, 'user_id', user_id)


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.User]:
    return await get_object_by_field(db, models.User, 'username', username)


async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate) -> Optional[schemas.User]:
    """Update an existing user."""
    async with db.begin():
        # 1. Fetch the User
        result = await db.execute(select(models.User).where(models.User.user_id == user_id))
        user = result.scalars().first()

        # 2. Check User Existence
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 3. Handle Password Separately
        update_data = user_update.dict(exclude_unset=True)  # Exclude unset fields
        if 'password' in update_data:
            # Hash password and update field name to password_hash
            update_data['password_hash'] = pwd_context.hash(update_data.pop('password'))

        # 4. Explicitly Define Fields to Update
        allowed_fields = ['username', 'email', 'password_hash', 'address', 'last_login']
        for field in allowed_fields:
            if field in update_data:
                setattr(user, field, update_data[field])

        # Update last_login to current UTC time if it's not included in the update_data
        if 'last_login' not in update_data:
            user.last_login = datetime.now(timezone.utc)

        try:
            # 5. Commit Changes
            await db.commit()
            await db.refresh(user)

            # 6. Return Updated User
            return schemas.User.from_orm(user)
        except IntegrityError as ie:
            logger.error(f"Integrity error while updating user {user_id}: {ie}")
            await db.rollback()  # Rollback changes in case of error
            raise HTTPException(status_code=400, detail="Integrity error, possibly due to duplicate entries.")
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            await db.rollback()  # Rollback changes in case of error
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

            # Convert the SQLAlchemy user model to a dictionary
            user_dict = {column.name: getattr(user, column.name) for column in models.User.__table__.columns}

            # Validate using model_validate with from_attributes=True
            return schemas.User.model_validate(user_dict, from_attributes=True)
        except IntegrityError as ie:
            logger.error(f"Integrity error while deleting user {user_id}: {ie}")
            await db.rollback()
            raise HTTPException(status_code=400, detail="Integrity error, possibly due to foreign key constraints.")
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            await db.rollback()
            raise HTTPException(status_code=500, detail="An error occurred while deleting the user.")


async def get_all_users(db: AsyncSession) -> List[schemas.User]:
    """Fetch all users."""
    try:
        result = await db.execute(select(models.User))
        users = result.scalars().all()
        return [schemas.User.from_orm(user) for user in users]
    except Exception as e:
        logger.error(f"Error fetching all users: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching users.")