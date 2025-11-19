from selenium.webdriver.common.by import By
from core.base_page import BasePage

class LoginPage(BasePage):
    """Page Object da página de login do SITAC."""

    # ---------------------------
    # Locators
    # ---------------------------
    URL = "https://crea-ma.sitac.com.br/app/view/pages/login/login.php#!"

    USERNAME = (By.CSS_SELECTOR, "#username")
    PASSWORD = (By.CSS_SELECTOR, "#password")
    LOGIN_BTN = (By.CSS_SELECTOR, "#submit")
    WELCOME_AVATAR = (By.CSS_SELECTOR, "#welcome_avatar")  # elemento que aparece após login

    # ---------------------------
    # Ações da página
    # ---------------------------
    def open_login(self):
        """Abre a página de login."""
        self.open(self.URL)

    def fill_username(self, username: str):
        self.type(self.USERNAME, username)

    def fill_password(self, password: str):
        self.type(self.PASSWORD, password)

    def submit(self):
        self.click(self.LOGIN_BTN)

    def login(self, username: str, password: str):
        """
        Ação de login completa.
        """
        self.fill_username(username)
        self.fill_password(password)
        self.submit()

    # ---------------------------
    # Verificação de login
    # ---------------------------
    def is_logged_in(self, timeout=10) -> bool:
        """
        Verifica se o login foi bem-sucedido.
        Consideramos que o avatar aparece após login.
        """
        try:
            self.wait_for(self.WELCOME_AVATAR, timeout=timeout)
            return True
        except:
            return False
