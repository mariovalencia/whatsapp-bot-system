
import requests

ERP_BASE_URL = "https://tu-erp.com/api"
ERP_TOKEN = "tu_token"

def create_ticket(subject, description, user_id):
    headers = {
        "Authorization": f"token {ERP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "subject": subject,
        "description": description,
        "customer": user_id
    }
    response = requests.post(f"{ERP_BASE_URL}/resource/Issue", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
