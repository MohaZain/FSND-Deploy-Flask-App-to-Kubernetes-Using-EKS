'''
Tests for jwt flask app.
'''
import os
import json
import pytest

import main
# export TOKEN=`curl -d '{"email":"gw.zain@gmail.com","password":"123456"}' -H "Content-Type: application/json" -X POST a6a9b0dd1a0534625a10ee92663a93b6-708325965.us-east-2.elb.amazonaws.com/auth  | jq -r '.token'`
# curl --request GET 'a6a9b0dd1a0534625a10ee92663a93b6-708325965.us-east-2.elb.amazonaws.com/contents' -H "Authorization: Bearer ${TOKEN}" | jq 
SECRET = 'YourJWTSecret'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzAyMzEwNjgsIm5iZiI6MTYyOTAyMTQ2OCwiZW1haWwiOiJndy56YWluQGdtYWlsLmNvbSJ9.nuZL0jRotoKKwHxZyKDRg47Qy4Oao10FlH_XH0Dgh00'
EMAIL = 'gw.zain@gmail.com  '
PASSWORD = '123456'

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client



def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None
