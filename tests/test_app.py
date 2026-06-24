from service_desk_app.app.models import User


# Tests password hashing and validation work correctly
def test_user_password():
    user = User(email="test@test.com", role="user")
    user.set_password("password123")

    assert user.check_password("password123") is True
    assert user.check_password("wrongpassword") is False


# Tests user attributes are stored correctly once created
def test_user_creation():
    user = User(email="example@test.com", role="analyst")

    assert user.email == "example@test.com"
    assert user.role == "analyst"


# Test that updating a password replaces the old one
def test_password_change():
    user = User(email="change@test.com", role="user")
    user.set_password("password123")

    user.set_password("newpassword123")

    assert user.check_password("newpassword123") is True
    assert user.check_password("password123") is False


# Tests that passwords are not stored as plain text
def test_password_is_not_plain_text():
    user = User(email="secure@test.com", role="user")
    user.set_password("password123")

    assert user.password_hash != "password123"