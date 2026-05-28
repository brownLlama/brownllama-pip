"""
Langdock API Call.

This module provides a class for generating responses using the Langdock API.
"""

from typing import ClassVar

import requests


class Langdock:
    """A class for generating responses using the Langdock API."""

    BASE_URL = "https://api.langdock.com"

    DEFAULT_MODELS: ClassVar[dict[str, str]] = {
        "gemini": "gemini-2.5-flash",
        "openai": "gpt-5.4-mini",
        "anthropic": "claude-sonnet-4-5-20250929",
    }

    def __init__(
        self,
        api_key: str,
        provider: str,
        model: str | None = None,
    ) -> None:
        """
        Initialize the Langdock class.

        Args:
            api_key (str): The API key for accessing the Langdock API.
            provider (str): One of 'gemini', 'openai', 'anthropic'.
            model (str | None): Optional model override.

        """
        self.api_key = api_key
        self.provider = provider
        self.model = model or self.DEFAULT_MODELS[provider]
        self.session = requests.Session()

    @property
    def _headers(self) -> dict:
        """
        Return provider-specific request headers.

        Returns:
            dict: A dictionary containing the Authorization and Content-Type headers.

        """
        auth = (
            f"Bearer {self.api_key}"
            if self.provider in {"anthropic", "openai"}
            else self.api_key
        )
        return {"Authorization": auth, "Content-Type": "application/json"}

    def _post(self, url: str, payload: dict) -> dict:
        """
        Send a POST request and return the parsed JSON response.

        Args:
            url (str): The endpoint URL to send the request to.
            payload (dict): The JSON payload to include in the request body.

        Returns:
            dict: The parsed JSON response from the API.

        Raises:
            HTTPError: If the response status code indicates an error.

        """
        response = self.session.post(
            url,
            json=payload,
            headers=self._headers,
            timeout=60,
        )
        if not response.ok:
            try:
                error_body = response.json()
            except ValueError:
                error_body = response.text
            msg = f"{response.status_code} {response.reason} — API error: {error_body}"
            raise requests.exceptions.HTTPError(msg, response=response)
        return response.json()

    def _gemini(self, prompt: str) -> dict:
        url = f"{self.BASE_URL}/google/eu/v1beta/models/{self.model}:generateContent"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        }
        return self._post(url, payload)

    def _openai(self, prompt: str) -> dict:
        url = f"{self.BASE_URL}/openai/eu/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        return self._post(url, payload)

    def _anthropic(self, prompt: str, max_tokens: int = 1024) -> dict:
        url = f"{self.BASE_URL}/anthropic/eu/v1/messages"
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        return self._post(url, payload)

    def langdock_response(self, prompt: str) -> dict:
        """
        Generate a response using the configured provider.

        Args:
            prompt (str): The input prompt.

        Returns:
            dict: The parsed JSON response from the provider.

        """
        handlers = {
            "gemini": self._gemini,
            "openai": self._openai,
            "anthropic": self._anthropic,
        }
        return handlers[self.provider](prompt)
