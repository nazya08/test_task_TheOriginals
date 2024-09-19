import argparse

from sqlalchemy.orm import Session

from src.adapters.repositories.user import UserRepository
from src.adapters.schemas.user import UserCreate
from src.adapters.sqlalchemy.db.session import SessionLocal
from src.adapters.sqlalchemy.models.user import UserType
from src.application.user.user_service import UserService


def create_superuser(
    email: str, password: str, username: str
):
    db_session: Session = SessionLocal()
    user_repo = UserRepository(session=db_session)
    user_service = UserService(user_repo=user_repo)
    try:
        superuser = UserCreate(
            email=email,
            password=password,
            username=username,
            is_active=True,
            type=UserType.admin,
        )

        user_service.create_user(superuser)
        print("Superuser successfully created")
        return

    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Create superuser")
    parser.add_argument(
        "email", type=str, help="Enter the email address for the superuser"
    )
    parser.add_argument(
        "password", type=str, help="Enter the password for the superuser"
    )
    parser.add_argument("username", type=str, help="Enter username")

    args = parser.parse_args()

    email = args.email
    password = args.password
    username = args.username

    create_superuser(email, password, username)


if __name__ == "__main__":
    main()
