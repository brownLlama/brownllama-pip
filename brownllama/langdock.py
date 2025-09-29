"""
Langdock API Call.

This module provides a class for generating responses, chat using the Langdock API.
"""

import requests


class Langdock:
    """A class for generating responses using the Langdock API."""

    def __init__(self, api_key: str, model: str | None = None) -> None:
        """
        Initialize the Langdock class.

        Args:
            api_key (str): The API key for accessing the Langdock API.
            model (str | None): Optional model name to use; defaults to "gpt-5-mini" if not provided.

        """
        self.url = "https://api.langdock.com/openai/eu/v1/chat/completions"
        self.headers = {"Authorization": api_key, "Content-Type": "application/json"}
        self.model = model or "gpt-5-mini"

    def generate_response(self, prompt: str, model: str | None = None) -> dict:
        """
        Generate a response using the GenAI API.

        Args:
            prompt (str): The prompt for generating the response.
            model (str | None): Optional model name to use for this request.
                                Defaults to the instance's model if not provided.

        Returns:
            The generated response.

        """
        payload = {
            "model": model or self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        }

        response = requests.post(
            self.url, json=payload, headers=self.headers, timeout=60
        )

        return response.json()
