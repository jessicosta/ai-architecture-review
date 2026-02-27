import os
from typing import Iterator
from google import genai
from .base import LLMClient


class GeminiClient(LLMClient):
    def __init__(
        self,
        model: str,
        temperature: float,
        max_output_tokens: int,
        api_key_env: str = "GOOGLE_API_KEY",
    ):
        if api_key_env not in os.environ:
            raise RuntimeError(f"{api_key_env} environment variable is not set")

        self.client = genai.Client(api_key=os.environ[api_key_env])
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def generate(self, prompt: str) -> Iterator[str]:
        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=prompt,
            config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_output_tokens,
            },
        ):
            if chunk.text:
                yield chunk.text