from typing import List

from models.User import User
from repository.database import get_db_connection
from service.api_service import get_users_from_api


def seed_users():
    all_users = find_all_users()
    if all_users and len(all_users) > 0:
        return
    users_list = get_users_from_api()
    list(map(lambda u: create_user(u), users_list))


def create_user(user: User) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO users (first, last, email)
            VALUES (%s, %s, %s) RETURNING id
        """, (user.first, user.last, user.email))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id


def find_all_users() -> List[User]:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            res = cursor.fetchall()
            users = [User(**u) for u in res]
            return users


def find_user_by_id(id_user: int) -> User | None:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (id_user,))
            res = cursor.fetchone()
            if res:
                return User(**res)
            else:
                return None


def delete_user(id_user: int):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (id_user,))
            connection.commit()


def update_user(user: User) -> User:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE users 
                SET first = %s, last = %s , email = %s
                WHERE id = %s
            """, (user.first, user.last, user.email, user.id))
            connection.commit()
    return user
