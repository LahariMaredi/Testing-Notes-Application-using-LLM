from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class NotesPage(BasePage):

    # Buttons
    ADD_NOTE_BTN = (By.CSS_SELECTOR, "button[data-testid='add-new-note']")
    ADD_NOTE_BTN_FALLBACK = (By.XPATH, "//button[contains(.,'Add')]")

    # Modal
    TITLE = (By.CSS_SELECTOR, "input[data-testid='note-title']")
    DESCRIPTION = (By.CSS_SELECTOR, "textarea[data-testid='note-description']")
    CREATE_BTN = (By.CSS_SELECTOR, "button[data-testid='note-submit']")

    # Notes list
    NOTE_CARD = (By.CSS_SELECTOR, "div[data-testid='note-card']")
    NOTE_TITLE = (By.CSS_SELECTOR, "div[data-testid='note-card-title']")
    DELETE_BTN = (By.CSS_SELECTOR, "button[data-testid='note-delete']")
    DELETE_CONFIRM_BTN = (By.CSS_SELECTOR, "button[data-testid='note-delete-confirm']")

    def click_add_note(self):
        # Use self-healing locator
        btn = self.find_with_fallback(self.ADD_NOTE_BTN, self.ADD_NOTE_BTN_FALLBACK)
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

    def create_note(self, title, description):
        self.wait.until(EC.visibility_of_element_located(self.TITLE))
        self.safe_type(self.TITLE, title)
        self.safe_type(self.DESCRIPTION, description)
        self.safe_click(self.CREATE_BTN)
        self.wait_for_note_present(title)

    def wait_for_note_present(self, title):
        note_locator = (
            By.XPATH,
            f"//div[@data-testid='note-card-title' and normalize-space(text())='{title}']"
        )
        self.wait.until(EC.visibility_of_element_located(note_locator))
        return True

    def is_note_present(self, title):
        """
        Check if note is present using exact match to avoid false positives.
        """
        elements = self.driver.find_elements(
            By.XPATH,
            f"//div[@data-testid='note-card-title' and normalize-space(text())='{title}']"
        )
        return len(elements) > 0

    def delete_note(self, title):
        # More stable locator: find note card containing the specific title
        note_card = self.driver.find_element(
            By.XPATH,
            f"//div[@data-testid='note-card'][.//div[@data-testid='note-card-title' and normalize-space(text())='{title}']]"
        )
        delete_btn = note_card.find_element(By.CSS_SELECTOR, "button[data-testid='note-delete']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", delete_btn)
        self.driver.execute_script("arguments[0].click();", delete_btn)

        # Wait for delete confirmation modal and click confirm button
        self.wait.until(EC.element_to_be_clickable(self.DELETE_CONFIRM_BTN))
        confirm_element = self.driver.find_element(*self.DELETE_CONFIRM_BTN)
        self.driver.execute_script("arguments[0].click();", confirm_element)

        # Wait for note to be removed
        self.wait.until(EC.staleness_of(note_card))
        self.wait.until(EC.invisibility_of_element_located(
            (By.XPATH, f"//div[@data-testid='note-card-title' and normalize-space(text())='{title}']")
        ))
