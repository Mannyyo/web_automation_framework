"""
BasePage — classe para o padrão Page Object Model (POM).
"""

from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple
from core.browser_manager import Browser


class BasePage:
    """
    Classe base para implementação do Page Object Model.
    Todas as páginas concretas devem herdar desta classe.
    Fornece métodos utilitários padronizados usando o
    BrowserManager como backend.
    """

    def __init__(self, browser: Browser):
        """
        Inicializa a página com uma instância do Browser.
        """
        if not isinstance(browser, Browser):
            raise TypeError("BasePage espera uma instância de Browser.")
        self.browser = browser

    # ----------------------------------------------------------------------
    # Métodos de ações
    # ----------------------------------------------------------------------

    def click(self, locator: Tuple[str, str], timeout: int = 10):
        """
        Clica em um elemento localizado pelo tuple (By, selector).
        """
        by, selector = locator
        return self.browser.click(selector, by=by, timeout=timeout)

    def type(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: int = 10):
        """
        Digita texto em um elemento (By, selector).
        """
        by, selector = locator
        return self.browser.type(
            selector,
            text,
            by=by,
            timeout=timeout,
            clear_first=clear_first,
        )

    def get_text(self, locator: Tuple[str, str], timeout: int = 10) -> str:
        """
        Retorna o texto de um elemento localizado.
        """
        by, selector = locator
        return self.browser.wait_for(selector, by=by, timeout=timeout)

    def wait_for(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        """
        Atalho: espera e retorna o WebElement.
        """
        by, selector = locator
        return self.browser.wait_for(selector, by=by, timeout=timeout)

    # ----------------------------------------------------------------------
    # Navegação (opcional por página)
    # ----------------------------------------------------------------------

    def open(self, url: str):
        """Abre uma URL diretamente."""
        self.browser.go_to(url)

    # ----------------------------------------------------------------------
    # Scroll e JS
    # ----------------------------------------------------------------------
    
    def scroll_to(self, locator: Tuple[str, str], timeout: int = 10):
        by, selector = locator
        return self.browser.scroll_to_element(selector, by=by, timeout=timeout)
    
    def execute_js(self, script: str, *args):
        return self.browser.execute_script(script, *args)
