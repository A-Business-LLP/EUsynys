import requests


response = requests.post("http://127.0.0.1:8000/api/v1/token/", data={"user_name": "heimu", "password": "leopoldfitz"})
print(response.text)

response = requests.get("http://127.0.0.1:8000/api/v1/user/region/tables/", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEwOTIzMjU0LCJpYXQiOjE3MTA5MTk2NTQsImp0aSI6ImYxOTUxOTc1Y2VlODRmOTlhMDQ1OTIzMWIyNmY4NjU2IiwidXNlcl9pZCI6MX0.ZZ2gb6rwjGdXBNVLBWsZYhnXJbdD1xX5D9kPvYJrW3Y"})
print(response.text)
