import requests

url = "http://localhost:5678/webhook/risk-alert"

data = {
    "risk_level": "HIGH",
    "document_type": "Private Investment Agreement"
}

response = requests.post(url, json=data)

print("Status:", response.status_code)
print("Response:", response.text)