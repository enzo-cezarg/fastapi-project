from http import HTTPStatus

from fastapi_project.schemas import UserPublic


def test_read_root_retorna_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'examplemail@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@mail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': 'password123',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': 1,
        },
    )

    assert response.json() == {
        'username': 'testusername2',
        'email': 'test@test.com',
        'id': 1,
    }


def test_update_user_exception(client, user):
    response = client.put(
        '/users/-1',
        json={
            'password': 'password123',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': -1,
        },
    )

    second_response = client.put(
        '/users/5',
        json={
            'password': 'password123',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': 5,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert second_response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}
    assert second_response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}


def test_delete_user_exception(client):
    response = client.delete('/users/-1')

    second_response = client.delete('/users/5')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert second_response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}
    assert second_response.json() == {'detail': 'User not found'}
