import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

url = 'https://www.ambitionbox.com/list-of-companies?page=1'

start_time = time.time()
response = requests.get(url, headers=headers)
end_time = time.time()

print(f"Time taken: {end_time - start_time} seconds")
print(response.text)