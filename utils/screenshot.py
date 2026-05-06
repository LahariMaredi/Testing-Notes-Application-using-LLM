import os
from datetime import datetime
import allure


def take_screenshot(driver, test_name):
    """
    Take screenshot and save with timestamp
    Returns screenshot file path
    """
    try:
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        
        driver.save_screenshot(filename)
        return filename
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None


def attach_screenshot_to_allure(driver, step_name):
    """
    Take screenshot and attach to Allure report
    """
    try:
        screenshot = driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name=step_name,
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        print(f"Error attaching screenshot to Allure: {e}")
