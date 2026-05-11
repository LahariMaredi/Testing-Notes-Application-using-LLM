import os
from datetime import datetime
from llm_automation.llm_client import GroqClient
from llm_automation.prompt_templates import LOCATOR_IMPROVEMENT_PROMPT, build_locator_prompt

class LocatorExpert:
    def __init__(self):
        self.client = GroqClient()
        self.reports_dir = "reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def suggest_locators(self, test_name: str, error_message: str, dom_source: str) -> str:
        """
        Analyzes the DOM to suggest more stable locators for the failing element.
        """
        print(f"\\n[AI Locator Expert] Analyzing DOM for: {test_name}...")
        
        user_prompt = build_locator_prompt(test_name, error_message, dom_source)
        
        try:
            suggestions = self.client.generate_code(LOCATOR_IMPROVEMENT_PROMPT, user_prompt, is_code=False)
            
            # Save the report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = test_name.replace("/", "_").replace("::", "_").replace(".py", "")
            filename = f"locator_suggestions_{safe_name}_{timestamp}.md"
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, "w") as f:
                f.write(f"# AI Locator Suggestions: {test_name}\\n\\n")
                f.write(suggestions)
                
            print(f"[AI Locator Expert] Suggestions saved to: {filepath}\\n")
            return suggestions
        except Exception as e:
            error_text = f"Failed to perform locator analysis: {e}"
            print(error_text)
            return error_text
