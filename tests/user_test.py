import pytest
from models.User import User
from repository.user_repository import find_all_users, create_user, find_user_by_id, update_user, delete_user


@pytest.fixture(scope="module")
def setup_database():
    users = find_all_users()
    return users


def test_find_all_users(setup_database):
    users = setup_database
    assert len(users) > 0, "No users found in the database"


def test_create_user():
    new_user = User(first="menachem", last="albert", email="ma05567@gmail.com")
    user_id = create_user(new_user)
    assert user_id is not None, "Failed to create a new user"


def test_find_user_by_id(setup_database):
    user = setup_database[0]
    found_user = find_user_by_id(user.id)
    assert found_user is not None, "User not found by id"


def test_update_user():
    updated_user = User(id=7, first="UpdatedFirst", last="UpdatedLast", email="updated@.com")
    update_user(updated_user)
    user_after_update = find_user_by_id(7)
    assert user_after_update is not None, "Failed to update the user"


def test_delete_user():
    delete_user(7)
    deleted_user = find_user_by_id(7)
    assert deleted_user is None, "User was not deleted"
