from sqlalchemy import Column, Integer, String, Enum
from app.database.base import Base
from app.auth.constants import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    password = Column(String(255), nullable=False)  # plain-text password (NOT RECOMMENDED for production)
    must_change_password = Column(Integer, default=1)  # 1 = must change

