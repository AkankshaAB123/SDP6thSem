import requests

def trigger_n8n(data):
    url = "http://localhost:5678/webhook/risk-alert"

    try:
        response = requests.post(url, json=data)
        print("n8n response:", response.status_code, response.text)
    except Exception as e:
        print("Error triggering n8n:", e)