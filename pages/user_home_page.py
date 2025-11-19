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
    MENU_PROTOCOLO_A_RECEBER = (By.CSS_SELECTOR, "#mostrarProtocolosAReceber")

    CATEGORIA_0 = (By.CSS_SELECTOR, "#mostrarProtocoloSetorFilial0")
    CATEGORIA_1 = (By.CSS_SELECTOR, "#mostrarProtocoloSetorFilial1")
    CATEGORIA_2 = (By.CSS_SELECTOR, "#mostrarProtocoloSetorFilial2")

    CATEGORIAS = {
        0: CATEGORIA_0,
        1: CATEGORIA_1,
        2: CATEGORIA_2,
    }

    # -----------------------------------
    # Ações de navegação
    # -----------------------------------

    def abrir_protocolos(self):
        self.click(self.MENU_PROTOCOLOS)

    def abrir_protocolos_a_receber(self):
        self.click(self.MENU_PROTOCOLO_A_RECEBER)

    def abrir_categoria(self, numero: int):
        if numero not in self.CATEGORIAS:
            raise ValueError(f"Setor '{numero}' não é válido. Use 0, 1 ou 2.")
        self.click(self.CATEGORIAS[numero])

    # -------- Métodos semânticos --------

    def abrir_aguardando_resposta_despacho(self):
        self.abrir_categoria(0)

    def abrir_departamento_fiscalizacao(self):
        self.abrir_categoria(1)

    def abrir_pre_envio_para_camaras(self):
        self.abrir_categoria(2)

    # -----------------------------------
    # Fluxo completo
    # -----------------------------------

    def acessar_categoria(self, categoria: int):
        """
        Fluxo completo:
        Home → Protocolos → A Receber → Categoria X
        """
        self.abrir_protocolos()
        self.abrir_protocolos_a_receber()
        self.abrir_categoria(categoria)
