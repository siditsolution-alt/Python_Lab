from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class OpenAIService:
    """Generic OpenAI service for API interactions."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client with API key."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=self.api_key)
    
    def create_completion(
        self,
        prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate a completion using OpenAI API.
        
        Args:
            prompt: The input prompt/message
            model: Model to use (default: gpt-4o-mini)
            temperature: Sampling temperature (0-2)
            top_p: Nucleus sampling parameter
            max_tokens: Maximum tokens in response
            
        Returns:
            The completion text response
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")


# Example usage
if __name__ == "__main__":
    service = OpenAIService()
    response = service.create_completion(
        prompt="Write a creative sentence about stars.",
        model="gpt-4o-mini",
        temperature=2.0,
        max_tokens=1000
    )
    print(response)