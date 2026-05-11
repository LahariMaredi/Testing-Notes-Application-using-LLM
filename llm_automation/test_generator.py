import os
import requests
from config.environment import config
from llm_automation.llm_client import GroqClient
from llm_automation.prompt_templates import SYSTEM_PROMPT, build_user_prompt

def fetch_html(url: str) -> str:
    """Fetches HTML content from the given URL."""
    print(f"Fetching code from: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return ""

def generate_test_scripts(html_content: str, output_dir="tests/generated_tests"):
    """
    Generates Pytest scripts based on HTML content using Groq.
    """
    if not html_content:
        print("No HTML content to analyze.")
        return
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        with open(os.path.join(output_dir, "__init__.py"), "w") as f:
            pass
            
    client = GroqClient()
    
    print("Analyzing HTML and calling Groq API...")
    user_prompt = build_user_prompt(html_content)
    generated_code = client.generate_code(SYSTEM_PROMPT, user_prompt)
    
    filepath = os.path.join(output_dir, "test_generated_from_html.py")
    
    with open(filepath, "w") as f:
        f.write(generated_code)
        
    print(f"Generated test suite saved to: {filepath}")

def main():
    base_url = config.get("base_url")
    if not base_url:
        print("base_url not found in config.yaml.")
        return
        
    html_content = fetch_html(base_url)
    generate_test_scripts(html_content)
    
    print("\nGeneration complete! You can run the generated tests using: pytest tests/generated_tests/")

if __name__ == "__main__":
    main()
