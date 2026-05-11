import os
from datetime import datetime
from llm_automation.llm_client import GroqClient
from llm_automation.prompt_templates import FAILURE_ANALYSIS_PROMPT, build_failure_prompt

class FailureAnalyzer:
    def __init__(self):
        self.client = GroqClient()
        self.reports_dir = "reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def analyze_failure(self, test_name: str, error_message: str) -> str:
        """
        Sends the error traceback to Groq for root cause analysis and saves the report.
        """
        print(f"\\n[AI Observer] Analyzing failure for: {test_name}...")
        
        user_prompt = build_failure_prompt(test_name, error_message)
        
        try:
            analysis = self.client.generate_code(FAILURE_ANALYSIS_PROMPT, user_prompt, is_code=False)
            
            # Save the report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = test_name.replace("/", "_").replace("::", "_").replace(".py", "")
            filename = f"failure_report_{safe_name}_{timestamp}.md"
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, "w") as f:
                f.write(f"# AI Root Cause Analysis: {test_name}\\n\\n")
                f.write(analysis)
                
            print(f"[AI Observer] Analysis saved to: {filepath}\\n")
            return analysis
        except Exception as e:
            error_text = f"Failed to perform AI analysis: {e}"
            print(error_text)
            return error_text
