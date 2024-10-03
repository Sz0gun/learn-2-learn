import os
import json
from google.cloud import secretmanager
from google.cloud import storage
from google.oauth2 import service_account  # Obsługa poświadczeń serwisowych

class GCPService:
    def __init__(self):
        self.project_id = self.get_secret("GCP_PROJECT_ID")
        print(f"Project ID: {self.project_id}")
        
        if not self.project_id:
            raise ValueError("Project ID could not be retrieved from Google Cloud Secret Manager.")

        # Pobieramy poświadczenia z sekretu "my-keyfile"
        self.credentials_json = self.get_secret("my-keyfile")
        if not self.credentials_json:
            raise ValueError("Credentials could not be retrieved from Google Cloud Secret Manager.")
        
        # Debugowanie zawartości JSON-a klucza serwisowego
        print(f"Credentials JSON: {self.credentials_json[:100]}...")  # Pokazujemy pierwsze 100 znaków
        
        self.client = None
        self._authorize_gcp()

    def get_secret(self, secret_name):
        """Retrieve secret value from Google Cloud Secret Manager."""
        client = secretmanager.SecretManagerServiceClient()
        secret_path = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        
        try:
            response = client.access_secret_version(request={"name": secret_path})
            secret_value = response.payload.data.decode("UTF-8")
            print(f"Retrieved secret {secret_name}: {secret_value[:10]}...")  # Wyświetlamy część sekretu do debugowania
            return secret_value
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            return None

    def _authorize_gcp(self):
        """Set up Google Cloud authorization using credentials directly from memory."""
        try:
            # Konwertujemy JSON na obiekt Python (dict)
            credentials_info = json.loads(self.credentials_json)
            
            # Tworzymy poświadczenia z JSON-a klucza serwisowego
            credentials = service_account.Credentials.from_service_account_info(credentials_info)

            # Inicjalizujemy klienta Google Cloud Storage z wczytanymi poświadczeniami
            self.client = storage.Client(credentials=credentials, project=self.project_id)  # Używamy credentials tutaj
            print("Authorization successful.")
        except Exception as e:
            print(f"Authorization error: {e}")
            raise

    def get_model_from_gcs(self, model_name, destination_path):
        """Download the model from Google Cloud Storage and save it locally."""
        bucket_name = 'm0dels_ai'
        
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(model_name)
            blob.download_to_filename(destination_path)
            print(f"Model {model_name} has been downloaded to {destination_path}")
        except Exception as e:
            print(f"Error downloading model from GCS: {e}")
            raise

# ---- TESTOWANIE KLASY ----

if __name__ == "__main__":
    try:
        # Tworzymy instancję klasy GCPService
        print("Creating GCPService instance...")
        gcp_service = GCPService()

        # Sprawdzamy, czy autoryzacja się powiodła
        print("Instance created and authorized successfully.")

        # Próbujemy pobrać model z GCS (przykład testowy)
        test_model_name = "example_model_name"  # Zmień na rzeczywistą nazwę modelu
        test_destination_path = "path/to/save/model"  # Zmień na rzeczywistą ścieżkę
        gcp_service.get_model_from_gcs(test_model_name, test_destination_path)

    except Exception as e:
        print(f"An error occurred during testing: {e}")
