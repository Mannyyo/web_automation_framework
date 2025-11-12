"""
BasePage — classe abstrata para o padrão Page Object Model (POM).

Define um contrato comum para todas as páginas do sistema,
garantindo consistência e encapsulando a interação com o Browser.
"""

from abc import ABC, abstractmethod
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple, Optional
from core.browser_manager import Browser


class BasePage(ABC):
    """
    Classe base abstrata para implementação do Page Object Model.
    Todas as páginas concretas devem herdar desta classe.
    """

    def __init__(self, browser: Browser):
        """
        Inicializa a página com uma instância do Browser.
        """
        if not isinstance(browser, Browser):
            raise TypeError("BasePage espera uma instância de Browser.")
        self.browser = browser

    # ----------------------------------------------------------------------
    # Métodos abstratos — devem ser implementados em subclasses
    # ----------------------------------------------------------------------

    @property
    @abstractmethod
    def URL(self) -> Optional[str]:
        """
        URL base da página.
        Deve ser implementado na subclasse (ou retornar None se não aplicável).
        """
        pass

    @abstractmethod
    def is_loaded(self) -> bool:
        """
        Deve retornar True se a página foi carregada corretamente.
        Pode validar a presença de um elemento, título, etc.
        """
        pass

    # ----------------------------------------------------------------------
    # Métodos utilitários concretos — herdados por todas as páginas
    # ----------------------------------------------------------------------

    def go_to(self, url: Optional[str] = None):
        """
        Navega até a URL da página.
        Se uma URL for passada, ela substitui o atributo URL.
        """
        target = url or self.URL
        if not target:
            raise ValueError("Nenhuma URL definida para esta página.")
        self.browser.go_to(target)

    def click(self, locator: Tuple[str, str], timeout: int = 10):
        """
        Clica em um elemento localizado pelo tuple (By, selector).
        """
        by, selector = locator
        el = self.browser.wait_for(selector, by=by, timeout=timeout)
        el.click()

    def type(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: int = 10):
        """
        Digita texto em um elemento (By, selector).
        """
        by, selector = locator
        el = self.browser.wait_for(selector, by=by, timeout=timeout)
        if clear_first:
            el.clear()
        el.send_keys(text)

    def text(self, locator: Tuple[str, str], timeout: int = 10) -> str:
        """
        Retorna o texto de um elemento localizado.
        """
        by, selector = locator
        el = self.browser.wait_for(selector, by=by, timeout=timeout)
        return el.text

    def wait_for(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        """
        Aguarda até que o elemento esteja presente no DOM e o retorna.
        """
        by, selector = locator
        return self.browser.wait_for(selector, by=by, timeout=timeout)

    def screenshot(self, path: str):
        """
        Captura uma screenshot da página atual.
        """
        self.browser.screenshot(path)

    def get_title(self) -> str:
        """
        Retorna o título atual da página.
        """
        return self.browser.driver.title

    def current_url(self) -> str:
        """
        Retorna a URL atual do navegador.
        """
        return self.browser.driver.current_url

    # ----------------------------------------------------------------------
    # Hooks opcionais — podem ser sobrescritos
    # ----------------------------------------------------------------------

    def before_action(self):
        """Executa antes de qualquer ação (ex: logs, verificação de sessão)."""
        pass

    def after_action(self):
        """Executa após qualquer ação (ex: verificação de erros, screenshots)."""
        pass
