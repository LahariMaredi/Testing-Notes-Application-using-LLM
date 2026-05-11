import os
from groq import Groq
from config.environment import config

class GroqClient:
    def __init__(self):
        self.api_key = config.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in config.yaml.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile" 

    def generate_code(self, system_prompt: str, user_prompt: str, is_code: bool = True) -> str:
        """
        Calls the Groq API to generate code based on the prompts.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                model=self.model,
                temperature=0.2, # Low temperature for more deterministic code generation
            )
            
            response = chat_completion.choices[0].message.content
            
            if is_code:
                # Clean up the markdown formatting if the LLM adds it
                if "```python" in response:
                    response = response.split("```python")[1].split("```")[0].strip()
                elif "```" in response:
                    response = response.split("```")[1].split("```")[0].strip()
                    
            return response
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            raise
