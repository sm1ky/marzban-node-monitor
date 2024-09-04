import httpx
import logging
import time
import redis
from .config import Config


class MarzbanAPI:
    def __init__(self):
        self.base_url = Config.MARZBAN_BASE_URL
        self.redis = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            password=Config.REDIS_PASSWORD)
        self.token_key = "marzban_access_token"
        self.token_expiry_key = "marzban_token_expiry"
        self.session = httpx.Client()
        self.auth_token = None

    def get_cached_token(self):
        token = self.redis.get(self.token_key)
        expiry = self.redis.get(self.token_expiry_key)

        if token and expiry and time.time() < float(expiry):
            logging.info(f"Using cached access token: {token.decode('utf-8')}")
            return token.decode('utf-8')
        else:
            return self.authenticate()

    def authenticate(self):
        try:
            response = self.session.post(
                f"{self.base_url}/admin/token",
                data={
                    "grant_type": "password",
                    "username": Config.MARZBAN_USERNAME,
                    "password": Config.MARZBAN_PASSWORD,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30.0
            )
            response.raise_for_status()
            token_data = response.json()
            self.auth_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 3600)
            self.redis.set(self.token_key, self.auth_token, ex=expires_in)
            self.redis.set(
                self.token_expiry_key,
                time.time() + expires_in,
                ex=expires_in)

            logging.info(
                msg=f"Authenticated successfully. New access token: {self.auth_token}")
            return self.auth_token
        except httpx.HTTPError as e:
            logging.error(f"Authentication failed: {e}")
            raise Exception(f"Authentication failed: {e}")

    def get_auth_headers(self):
        token = self.get_cached_token()
        return {"Authorization": f"Bearer {token}"}

    def get_nodes(self):
        try:
            headers = self.get_auth_headers()
            response = self.session.get(
                f"{self.base_url}/nodes", headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to retrieve nodes: {e}")

    def get_node(self, node_id):
        try:
            headers = self.get_auth_headers()
            response = self.session.get(
                f"{self.base_url}/node/{node_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to retrieve node {node_id}: {e}")

    def reconnect_node(self, node_id):
        try:
            headers = self.get_auth_headers()
            response = self.session.post(
                f"{self.base_url}/node/{node_id}/reconnect", headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to reconnect node {node_id}: {e}")
