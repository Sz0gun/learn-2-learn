import subprocess
import json
from datetime import datetime

def gcloud_login():
    # Logowanie do Google Cloud
    subprocess.run(["gcloud", "auth", "login"], check=True)

def delete_service_account_key(service_account_email, key_id):
    # Usuwanie klucza
    print(f"Deleting key {key_id} for service account {service_account_email}")
    subprocess.run(
        ["gcloud", "iam", "service-accounts", "keys", "delete", key_id, "--iam-account", service_account_email],
        check=True
    )

def create_service_account_key(service_account_email):
    # Tworzenie nowego klucza
    print(f"Creating a new key for service account: {service_account_email}")
    subprocess.run(
        ["gcloud", "iam", "service-accounts", "keys", "create", "new-key.json", "--iam-account", service_account_email],
        check=True
    )

def delete_old_keys(service_account_email, keys):
    # Usuwanie kluczy z krótką datą ważności
    now = datetime.utcnow()
    for key in keys:
        expiry = key.get('validBeforeTime')
        if expiry:
            expiry_date = datetime.strptime(expiry, "%Y-%m-%dT%H:%M:%SZ")
            if (expiry_date - now).days < 7:
                delete_service_account_key(service_account_email, key['name'])

def get_service_account_keys(service_account_email):
    result = subprocess.run(
        ["gcloud", "iam", "service-accounts", "keys", "list", "--iam-account", service_account_email, "--format=json"],
        check=True, capture_output=True, text=True
    )
    return json.loads(result.stdout)

def main():
    project_id = "ai-chatbot-project-431422"
    
    # Logowanie
    gcloud_login()

    # Przykładowe konto serwisowe
    service_account_email = "learn-2-learn@ai-chatbot-project-431422.iam.gserviceaccount.com"
    
    # Pobieranie kluczy
    keys = get_service_account_keys(service_account_email)
    
    # Usuwanie starych kluczy
    delete_old_keys(service_account_email, keys)
    
    # Tworzenie nowego klucza
    create_service_account_key(service_account_email)

if __name__ == "__main__":
    main()
