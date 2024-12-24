import hvac
import os
import logging
from elasticsearch import Elasticsearch
import hvac.exceptions

class FabricControlUtils:
    def __init__(self):
        # Logger for fallback logging
        self.logger = logging.getLogger("django")

        # Vault configuration
        self.vault_host = os.getenv('VAULT_ADDR')
        self.vault_token = os.getenv('VAULT_TOKEN')
        self.vault_client = self._init_vault_client()

        # Elasticsearch configuration
        self.elasticsearch_host = os.getenv("ELASTICSEARCH_HOST")
        self.elasticsearch_index = os.getenv("ELASTICSEARCH_INDEX", 'django-logs')
        self.elasticsearch_client = self._init_elasticsearch_client()


    def _init_vault_client(self):
        """ Initialize Vault client."""
        try:
            client = hvac.Client(url=self.vault_host, token=self.vault_token)
            if not client.is_authenticated():
                raise ConnectionError("Failed to authenticate with Vault.")
            return client
        except Exception as e:
            self.logger.error(f"Error initializing Vault client: {e}")
            raise

    def _init_elasticsearch_client(self):
        """ Initialize Elasticsearch client."""
        try:
            return Elasticsearch([self.elasticserach_host])
        except Exception as e:
            self.logger.error(f"Error initializing Elasticsearch client: {e}")
            raise

    def get_vault_secret(self, path):
        """
        Retrieve a secret from Vault.
        :param path: Path to the secret in Vault.
        :return: Secret data.
        """
        try:
            secret = self.vault_client.secrets.kv.v2.read_secret_version(path=path)
            return secret['data']['data']
        except Exception as e:
            self.logger.error(f"Failed to retrieve secret from Vault: {e}")
            raise

    def add_key_to_vault(self, path, key, value):
        """
        Add a key-value pair to Vault.
        :param path: Path in Vault where the key will be stored.
        :param key: Key name.
        :param value: Value to store.
        """
        try:
            secret_data = {key: value}
            self.vault_client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=secret_data
            )
            self.logger.info(f"Key '{key}' successfully added to Vault at '{path}'.")
        except Exception as e:
            self.logger.error(f"Failed to add key to Vault: {e}")
            raise
    
    def validate_vault_key_existence(self, path, key):
        """
        Validate if a key exists in Vault.
        :param path: Path in Vault where the key is stored.
        :param key: Key name to validate.
        :return: True if the key exists, False otherwise.
        """
        try:
            secret = self.vault_client.secrets.kv.v2.resd_secret_version(path=path)
            return key in secret['data']['data']
        except hvac.exceptions.InvalidPath:
            return False
        except Exception as e:
            self.logger.error(f"Error validating key eistence in Vault: {e}")
            raise

    def log_to_elasticsearch(self, message, level="info"):
        """
        Log a message to Elasticsearch and fallback to Django logging if needed.
        :param message: Message to log.
        :param level: Log level (info, warning, error, etc.).
        """
        try:
            self.elasticserach_client.index(
                index=self.elasticserach_index,
                body={
                    "message": message,
                    "level": level.upper(),
                    "timestamp": logging.Formatter().formatTime(logging.LogRecord("", 0, "", 0, None, None))
                }
            )
        except Exception as e:
            self.logger.error(f"Failed to log to Elasticsearch: {e}")

        # Fallback to Django logger
        getattr(self.logger, level.lower(), self.logger.info)(message)