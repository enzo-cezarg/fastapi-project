from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_project.app import app


def test_read_root_retorna_ok_e_ola_mundo():
    # Exemplo de teste Triple A
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá mundo!'}  # Assert
