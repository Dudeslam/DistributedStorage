import requests
import base64

k = 3
file_name = "1KB.txt"
url_stratAStore = f"http://localhost:9000/exercise2/files/{k}"
filepath = f"../testfiles/{file_name}"

data = open(filepath, "rb").read()
encoded = base64.b64encode(data).decode()


data = {"filename" : f"testfiles/{file_name}",
        "content_type": "text/plain",
        "contents_b64": encoded }

number_of_test_runs = 100

for _ in range(number_of_test_runs):
    response = requests.post(url_stratAStore, json=data)


