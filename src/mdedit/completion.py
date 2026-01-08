"""AI completion provider using llama.cpp server for PyWebView."""

import json
import logging
from typing import Callable, Optional

import requests


class LlamaCppCompletionProvider:
    """AI completion provider using llama.cpp server for PyWebView."""

    def __init__(self, server_url: str = "http://192.168.3.190:11434"):
        """
        Initialize the completion provider.

        Args:
            server_url: URL of the llama.cpp server
        """
        self.server_url = server_url.rstrip("/")
        self.timeout = 40

    def complete_helper(self, payload: dict) -> str:
        """
        Helper method to send completion request.

        Args:
            payload: The request payload

        Returns:
            Completed text
        """
        try:
            response = requests.post(
                f"{self.server_url}/completion", json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data.get("content", "")
        except requests.RequestException as e:
            logging.error("Completion request error: %s", str(e))
            return f"Error: {str(e)}"

    def complete(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        stop: Optional[list] = None,
    ) -> str:
        """
        Get completion from llama.cpp server.

        Args:
            prompt: The text to complete
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stop: Stop sequences

        Returns:
            Completed text
        """
        payload = {
            "prompt": prompt,
            "n_predict": max_tokens,
            "temperature": temperature,
            "stop": stop or [],
            "stream": False,
        }
        return self.complete_helper(payload)

    def complete_fim(
        self,
        prefix: str,
        suffix: str,
        max_tokens: int = 100,
        temperature: float = 0.7,
        stop: Optional[list] = None,
    ) -> str:
        """
        Get fill-in-the-middle completion from llama.cpp server.

        Args:
            prefix: The text before the gap
            suffix: The text after the gap
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stop: Stop sequences

        Returns:
            Completed text
        """
        payload = {
            "prompt": prefix,
            "input_prefix": prefix,
            "input_suffix": suffix,
            "n_predict": max_tokens,
            "temperature": temperature,
            "stop": stop or [],
            "stream": False,
        }
        return self.complete_helper(payload)

    def decode_stream_line(self, line: bytes) -> Optional[str]:
        """
        Decode a line from the stream.

        Args:
            line: The line bytes

        Returns:
            Decoded content or None
        """
        try:
            decoded = line.decode("utf-8").strip()
            if decoded.startswith("data: "):
                data = json.loads(decoded[6:])
                return data.get("content")
        except (json.JSONDecodeError, UnicodeDecodeError):
            logging.error("Failed to decode stream line")
            return "Error: Failed to decode stream line"
        return None

    def complete_stream_helper(
        self,
        payload: dict,
        callback: Callable[[str], None],
    ) -> None:
        """
        Helper method to stream completion with callback.
        Args:
            payload: The request payload
            callback: Function called with each chunk
        """
        try:
            response = requests.post(
                f"{self.server_url}/completion", json=payload, stream=True, timeout=60
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    content = self.decode_stream_line(line)
                    if content:
                        callback(content)
        except requests.RequestException as e:
            logging.error("Stream completion error: %s", str(e))
            callback(f"Error: {str(e)}")

    def complete_stream(
        self,
        prompt: str,
        callback: Callable[[str], None],
        max_tokens: int = 100,
        temperature: float = 0.7,
        stop: Optional[list] = None,
    ) -> None:
        """
        Stream completion from llama.cpp server with callback.

        Args:
            prompt: The text to complete
            callback: Function called with each chunk
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stop: Stop sequences
        """
        payload = {
            "prompt": prompt,
            "n_predict": max_tokens,
            "temperature": temperature,
            "stop": stop or [],
            "stream": True,
        }
        self.complete_stream_helper(payload, callback)

    def complete_fim_stream(
        self,
        prefix: str,
        suffix: str,
        callback: Callable[[str], None],
        max_tokens: int = 100,
        temperature: float = 0.7,
        stop: Optional[list] = None,
    ) -> None:
        """
        Stream fill-in-the-middle completion from llama.cpp server with callback.

        Args:
            prefix: The text before the gap
            suffix: The text after the gap
            callback: Function called with each chunk
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stop: Stop sequences
        """
        payload = {
            "prompt": prefix,
            "input_prefix": prefix,
            "input_suffix": suffix,
            "n_predict": max_tokens,
            "temperature": temperature,
            "stop": stop or [],
            "stream": True,
        }
        self.complete_stream_helper(payload, callback)
