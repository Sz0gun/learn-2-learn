# telegram_bot/gcs_auth.py - get_model_from_gcs - Dodano funkcję do pobierania modelu ESRGAN z GCS

import os
from google.cloud import storage

class GCPService:
    def __init__(self):
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.client = None
        self._authorize_gcp()

    def _authorize_gcp(self):
        """Set up Google Cloud authorization using local credentials"""
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
            self.client = storage.Client(project=self.project_id)
            print("Authorization successful.")
        except Exception as e:
            print(f"Authorization error: {e}")

    def get_model_from_gcs(self, model_name, destination_path):
        """Download the ESRGAN model from GCS and save it locally"""
        bucket_name = 'm0dels_ai'
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(model_name)
            blob.download_to_filename(destination_path)
            print(f"Model {model_name} has been downloaded to {destination_path}")
        except Exception as e:
            print(f"Error downloading model from GCS: {e}")
