from selenium.webdriver.common.by import By
from core.base_page import BasePage

class UserHomePage(BasePage):
    """
    Página inicial do SITAC após o login.
    Responsável pela navegação via menu lateral.
    """

    # -----------------------------------
    # Locators da barra lateral
    # -----------------------------------

    MENU_PROTOCOLOS = (By.CSS_SELECTOR, "#conteudo > div.cad_conteudo > div:nth-child(5)")
    MENU_A_RECEBER = (By.CSS_SELECTOR, "#mostrarProtocolosAReceber")

    SETOR_FILIAL_0 = (By.CSS_SELECTOR, "#mostrarProtocoloSetorFilial0")
    SETOR_FILIAL_1 = (By.CSS_SELECTOR, "#mostrarProtocoloSetorFilial1")
    SETOR_FILIAL_2 = (By.CSS_SELECTOR, "#mostrarProtocoloSetorFilial2")

    SETORES = {
        0: SETOR_FILIAL_0,
        1: SETOR_FILIAL_1,
        2: SETOR_FILIAL_2,
    }

    # -----------------------------------
    # Ações de navegação
    # -----------------------------------

    def abrir_protocolos(self):
        self.click(self.MENU_PROTOCOLOS)

    def abrir_protocolos_a_receber(self):
        self.click(self.MENU_A_RECEBER)

    def abrir_setor_filial(self, numero: int):
        if numero not in self.SETORES:
            raise ValueError(f"Setor '{numero}' não é válido. Use 1, 2 ou 3.")
        self.click(self.SETORES[numero])

    # -----------------------------------
    # Fluxo completo
    # -----------------------------------

    def acessar_protocolos_setor(self, setor: int):
        """
        Fluxo completo:
        Home → Protocolos → A Receber → Setor X
        """
        self.abrir_protocolos()
        self.abrir_protocolos_a_receber()
        self.abrir_setor_filial(setor)
