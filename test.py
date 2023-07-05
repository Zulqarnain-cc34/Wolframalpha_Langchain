import requests

url = "http://172.17.0.2:5000/prompt"

headers = {
    'Content-Type': 'application/json',
    'API-KEY': 'API-KEY'
}

data = {'prompt': '1+1'}

response = requests.post(url, headers=headers, json=data)

print(response.text)
