from selenium.webdriver.common.by import By
from core.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://crea-ma.sitac.com.br/app/view/pages/login/login.php#!"

    USERNAME = (By.CSS_SELECTOR, "#username")
    PASSWORD = (By.CSS_SELECTOR, "#password")
    LOGIN_BTN = (By.CSS_SELECTOR, "#submit")

    def is_loaded(self) -> bool:
        """Confirma se o campo de login está visível."""
        try:
            self.browser.wait_for(self.USERNAME[1], by=self.USERNAME[0], timeout=5)
            return True
        except Exception:
            return False

    def login(self, user: str, password: str):
        """Executa o login e retorna a próxima página."""
        self.type(self.USERNAME, user)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        from pages.user_home_page import UserPage
        return UserPage(self.browser)