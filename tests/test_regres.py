

import requests
from datetime import datetime

BASE_URL = 'https://reqres.in/'


def test_single_user_not_found():
    response = requests.get(url=BASE_URL + 'api/users/13')

    assert response.status_code == 404
    assert response.text == '{}'


def test_list_users_check_content_type_equals_json():
    page = 2

    response = requests.get(url=BASE_URL + 'api/users', params={'page': page})

    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json; charset=utf-8"


def test_create_user_with_current_date():
    cur_date = datetime.now().date()
    payload = {"name": "morpheus",
               "job": "leader"}

    response = requests.post(url=BASE_URL + 'api/users', json=payload)
    assert response.status_code == 201
    assert datetime.strptime(response.json()['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ').date() == cur_date


def test_create_user():
    payload = {"name": "Aleksandr",
               "job": "engineer"}
    response = requests.post(url=BASE_URL + 'api/users', json=payload)

    assert response.status_code == 201
    assert response.json()['name'] == 'Aleksandr'
    assert response.json()['job'] == 'engineer'

    return response.json()['id']


def test_update_user():
    id_user = test_create_user()
    payload = {"name": "Aleksandr",
               "job": "AutomationQA"}
    response = requests.put(url=BASE_URL + 'api/users/' + id_user, json=payload)

    assert response.status_code == 200
    assert response.json()['name'] == 'Aleksandr'
    assert response.json()['job'] == 'AutomationQA'


def test_delete_user():
    id_user = test_create_user()

    response = requests.delete(url=BASE_URL + 'api/users/' + id_user)

    assert response.status_code == 204
    assert response.headers['Content-Length'] == '0'


def test_register_successful():
    pyload = {"email": "eve.holt@reqres.in",
              "password": "pistol"}

    response = requests.post(url=BASE_URL + 'api/register', json=pyload)

    assert response.status_code == 200
    assert response.json()['id'] == 4
    assert response.json()['token'] == "QpwL5tke4Pnpja7X4"


def test_register_unsuccessful():
    pyload = {"email": "sydney@fife"}

    response = requests.post(url=BASE_URL + 'api/register', json=pyload)

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_login_successful():
    pyload = {"email": "eve.holt@reqres.in",
              "password": "cityslicka"}

    response = requests.post(url=BASE_URL + 'api/login', json=pyload)

    assert response.status_code == 200
    assert 'token' in response.json()
    assert response.json()['token'] == "QpwL5tke4Pnpja7X4"


def test_login_unsuccessful():
    pyload = {"email": "eve.holt@reqres.in"}

    response = requests.post(url=BASE_URL + 'api/login', json=pyload)

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
