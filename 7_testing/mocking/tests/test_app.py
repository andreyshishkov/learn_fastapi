import unittest
from unittest.mock import patch, MagicMock
from fastapi import status, HTTPException
from fastapi.testclient import TestClient


from app.main import app
from app.models import User


client = TestClient(app)


class TestMain(unittest.TestCase):

    @patch('app.db.create_user')
    def test_create_user(self, mock_db_create_user: MagicMock):
        mock_response = {
            'name': 'user1',
            'email': 'add@mail.ru',
            'phone': '567899',
        }
        mock_db_create_user.return_value = mock_response

        user_json = {
            'name': 'user1',
            'email': 'add@mail.ru',
            'phone': '567899',
        }
        response = client.post('/create_user', json=user_json)

        mock_db_create_user.assert_called_once_with(User(**user_json))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), mock_response)

    @patch('app.db.create_user')
    def test_create_user_error(self, mock_db_create_user: MagicMock):
        def mocked_response(ignored):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='error')

        mock_db_create_user.side_effect = mocked_response

        user_json = {
            'name': 'user2',
            'email': 'user2@mail.ru',
            'phone': '111111',
        }
        response = client.post('/create_user', json=user_json)

        mock_db_create_user.assert_called_once_with(User(**user_json))
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json(), {'detail': 'error'})

    @patch('app.db.get_user')
    def test_get_user(self, mock_db_get_user: MagicMock):
        mock_response = {
            'name': 'user1',
            'email': 'add@mail.ru',
            'phone': '567899',
        }
        mock_db_get_user.return_value = mock_response

        name = 'user1'
        response = client.get(f'/get_user/{name}')

        mock_db_get_user.assert_called_once_with(name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), mock_response)

    @patch('app.db.delete_user')
    def test_delete_user(self, mock_db_delete_user: MagicMock):
        username = 'user1'
        response = client.delete(f'/delete_user/{username}')

        mock_db_delete_user.assert_called_once_with(username)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
