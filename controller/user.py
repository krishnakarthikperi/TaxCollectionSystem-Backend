from db import SessionDep
from objects.user import User

def getUserByUsername(
        username: str,
        db: SessionDep
):
    return db.get(User, username)