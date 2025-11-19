from selenium.webdriver.common.by import By
from core.base_page import BasePage


class NoticiaModal(BasePage):
    """
    Componente que representa o modal de notícias exibido após o login.
    """

    MODAL = (By.ID, "modal-noticias")
    BTN_FECHAR = (By.CSS_SELECTOR, ".iziModal-button-close")

    def is_visible(self, timeout=3):
        """
        Retorna True se o modal estiver visível.
        """
        try:
            el = self.wait_for(self.MODAL, timeout=timeout)
            return el.is_displayed()
        except:
            return False

    def fechar(self):
        """
        Fecha o modal, caso esteja visível.
        """
        if self.is_visible():
            self.click(self.BTN_FECHAR)
