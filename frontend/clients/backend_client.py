import httpx

class BackendApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_status(self):
        response = httpx.get(f"{self.base_url}/api/status")
        response.raise_for_status()
        return response.json()

    def get_items(self):
        response = httpx.get(f"{self.base_url}/api/items")
        response.raise_for_status()
        return response.json()