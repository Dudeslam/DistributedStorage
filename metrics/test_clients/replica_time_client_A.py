import requests
import base64

k = 3
file_name = "10MB.txt"
url_stratAStore = f"http://62.107.0.222:9000/exercise2/files/{k}"
filepath = f"../testfiles/{file_name}"

data = open(filepath, "rb").read()
encoded = base64.b64encode(data).decode()


data = {"filename" : f"testfiles/{file_name}",
        "content_type": "text/plain",
        "contents_b64": encoded }

number_of_test_runs = 100

for i in range(number_of_test_runs):
    print(f"{i}/100")
    response = requests.post(url_stratAStore, json=data)


