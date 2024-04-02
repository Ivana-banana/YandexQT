import requests

print(
    requests.post("http://127.0.0.1/api/v2/users/",
                  json={
                      'name': 'Sonya',
                      'surname': "Red",
                      "age": 18,
                      'position': "biologist",
                      "speciality": 'pathologist',
                      'address': 'module 2',
                      'email': 'Q@q.com',
                      "hashed_password": "321"
                  })
)