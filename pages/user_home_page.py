from selenium.webdriver.common.by import By
from core.base_page import BasePage

class UserPage(BasePage):
    URL = "https://crea-ma.sitac.com.br/app/view/sight/ini?form=Pessoal&usuario={}"

    WELCOME_AVATAR = (By.CSS_SELECTOR, "#welcome_avatar")

    def is_loaded(self) -> bool:
        """Confirma se o campo de login está visível."""
        try:
            self.browser.wait_for(self.WELCOME_AVATAR[1], by=self.WELCOME_AVATAR[0], timeout=5)
            return True
        except Exception:
            return False