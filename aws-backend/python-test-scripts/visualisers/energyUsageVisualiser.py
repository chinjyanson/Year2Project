import requests

url = "https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessEnergyLog"

response = requests.get(url)
data = response.json()
print(data)

num_elements = len(data)

print(f"Number of elements returned: {num_elements}")