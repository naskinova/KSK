from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ✅ Use your actual MySQL DB
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://irina:1gabbie1@localhost:3306/ksk"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
