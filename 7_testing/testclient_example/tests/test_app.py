from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.models import User


client = TestClient(app)


def test_create_user():
    user_json = {
        "username": "name",
        "email": "add@mail.ru",
        "phone": "89902222",
    }
    response = client.post('/reg_user/', json=user_json)

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json is not None
    assert response_json == user_json


def test_create_same_users():
    user_json = {
        "username": "name1",
        "email": "add1@mail.ru",
        "phone": "89902222",
    }

    response = client.post('/reg_user/', json=user_json)
    assert response.status_code == status.HTTP_200_OK

    response = client.post('/reg_user/', json=user_json)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_missing_field():
    user_json = {
        "username": "name",
        "email": "add@mail.ru",
    }

    response = client.post('/reg_user/', json=user_json)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_user():
    username = 'andrey'
    user = User(username='andrey', email='333@mail.ru', phone='899992333')

    response = client.get(f'/get_user?username={username}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user.model_dump()


def test_get_not_fount_user():
    username = 'ivan'
    response = client.get(f'/get_user?username={username}')

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user():
    username = 'andrey'
    response = client.delete(f'/delete_user/{username}')
    assert response.status_code == status.HTTP_200_OK


def test_delete_contact_not_found():
    username = 'egor'
    response = client.delete(f'/delete_user/{username}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
