from pages.login_page import LoginPage
from pages.user_home_page import UserHomePage
from components.noticia_modal import NoticiaModal

class ConsultarProtocolosFlow:
    """
    Fluxo:
    Login → Fechar modal → Home → Protocolos → A Receber → Categoria semântica
    """

    def __init__(self, browser):
        self.browser = browser

        self.login_page = LoginPage(browser)
        self.home_page = UserHomePage(browser)
        self.modal_noticias = NoticiaModal(browser)

    # -----------------------------------------
    # Fluxo de login
    # -----------------------------------------
    def login(self, username: str, password: str):
        self.login_page.open_login()
        self.login_page.login(username, password)

        if not self.login_page.is_logged_in():
            raise RuntimeError("Falha no login.")

        self.modal_noticias.fechar()

    # -----------------------------------------
    # Métodos de fluxo semântico
    # -----------------------------------------
    def acessar_protocolos_aguardando_resposta_despacho(self):
        self.home_page.abrir_protocolos()
        self.home_page.abrir_protocolos_a_receber()
        self.home_page.abrir_aguardando_resposta_despacho()

    def acessar_protocolos_departamento_fiscalizacao(self):
        self.home_page.abrir_protocolos()
        self.home_page.abrir_protocolos_a_receber()
        self.home_page.abrir_departamento_fiscalizacao()

    def acessar_protocolos_pre_envio_para_camaras(self):
        self.home_page.abrir_protocolos()
        self.home_page.abrir_protocolos_a_receber()
        self.home_page.abrir_pre_envio_para_camaras()

    # -----------------------------------------
    # Fluxo completo com categoria semântica
    # -----------------------------------------
    def executar_fluxo_despacho(self, username: str, password: str):
        self.login(username, password)
        self.acessar_protocolos_aguardando_resposta_despacho()

    def executar_fluxo_fiscalizacao(self, username: str, password: str):
        self.login(username, password)
        self.acessar_protocolos_departamento_fiscalizacao()
    
    def executar_fluxo_pre_envio_camaras(self, username: str, password: str):
        self.login(username, password)
        self.acessar_protocolos_pre_envio_para_camaras()
