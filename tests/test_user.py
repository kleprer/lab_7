from fastapi.testclient import TestClient

from src.main import app
from src.schemas.user import CreateUser, UserInfo

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email':'jesuschrist@god.com'})
    assert response.statuc_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    test_user = CreateUser(name="test user", email="test@test.com")
    response = client.post("/users", json=test_user.dict())
    assert response.status_code = 201


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    test_user = CreateUser(name="Petr Petrov", email="p.p.petrov@mail.com")
    response = client.post("",json=test_user.dict())
    assert response.status_code=409
    assert response.json() = {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    response = client.delete("", params={"email":"p.p.petrov@mail.com"})
    assert response.status_code == 204
    assert response.content = b''
