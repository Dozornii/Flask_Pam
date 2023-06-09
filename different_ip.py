import requests

# Set the desired source IP address
source_ip = '192.168.0.100'

# Set the URL for the GET request
url = 'http://localhost:5000/login'

# Create a session and configure it to use the desired source IP address
session = requests.Session()
session.get(url, proxies={'http': 'http://'+source_ip}, source_address=(source_ip, 0))

# Send the GET request
response = session.get(url)

# Print the response
print(response.text)