import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

from core.browser_manager import Browser
from pages.login_page import LoginPage

browser = Browser(browser="chrome", headless=False)
login = LoginPage(browser)

login.open_login()
login.login("meu_usuario", "minha_senha")

if login.is_logged_in():
    print("Login realizado com sucesso!")
else:
    print("Falha no login.")

browser.quit()
