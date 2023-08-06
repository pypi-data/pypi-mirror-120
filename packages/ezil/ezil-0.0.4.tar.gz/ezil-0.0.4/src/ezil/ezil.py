"""EZIL mining pool API wrapper."""
from datetime import datetime, timedelta
import requests


class Ezil:
    """Ezil Class API wrapper."""

    def __init__(self):
        """Initialize the class."""
        self.endpoint = "https://{}.ezil.me/{}"
        self.endpointStats = self.endpoint.format("stats", "current_stats/{}/reported")
        self.endpointBilling = self.endpoint.format("billing", "balances/{}")
        self.endpointForecast = self.endpoint.format("billing", "forecasts_with_hashrate/{}")
        self.endpointHistory = self.endpoint.format("stats", "historical_stats/{}?time_from={}&time_to={}")

    def _get_data(self, endpoint: str) -> dict:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()

        return None

    def pool_stats(self, wallet) -> dict:
        """Get pool current stats."""
        return self._get_data(self.endpointStats.format(wallet))

    def pool_balance(self, wallet) -> dict:
        """Get pool balances."""
        return self._get_data(self.endpointBilling.format(wallet))

    def pool_forecast(self, wallet) -> dict:
        """Get pool forecast."""
        return self._get_data(self.endpointForecast.format(wallet))

    def pool_history(self, wallet) -> dict:
        """Get pool hashrate history."""
        date_now = datetime.now()
        date_to = date_now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        date_from = (date_now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        return self._get_data(self.endpointHistory.format(wallet, date_from, date_to))