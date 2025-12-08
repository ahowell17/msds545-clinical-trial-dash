from app.db.session import Base, engine, SessionLocal
from app.db import models
from app.core.security import get_password_hash

def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    def get_or_create(username: str, role: str):
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            user = models.User(
                username=username,
                role=role,
                hashed_password=get_password_hash("password123"),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created user {username} with role {role} and password 'password123'")
        else:
            print(f"User {username} already exists")

    get_or_create("uploader1", "uploader")
    get_or_create("viewer1", "viewer")
    db.close()
    print("Done.")

if __name__ == "__main__":
    init()
