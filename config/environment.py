import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config():
    with open("config/config.yaml") as f:
        cfg = yaml.safe_load(f)
    
    # Override GROQ_API_KEY with environment variable if available
    if "GROQ_API_KEY" in cfg:
        # Replace placeholder with actual environment variable
        api_key_from_env = os.getenv("GROQ_API_KEY")
        if api_key_from_env:
            cfg["GROQ_API_KEY"] = api_key_from_env
        elif cfg["GROQ_API_KEY"] == "${GROQ_API_KEY}":
            # If still placeholder and no env var, it will fail in GroqClient
            cfg["GROQ_API_KEY"] = None
    
    return cfg

config = load_config()
