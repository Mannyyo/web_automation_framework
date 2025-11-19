import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

from core.browser_manager import Browser
from flows.consultar_protocolos_flow import ConsultarProtocolosFlow

browser = Browser(browser="chrome", headless=False)

flow = ConsultarProtocolosFlow(browser)

flow.executar_fluxo_fiscalizacao(
    username="meu_usuario",
    password="minha_senha",
)

browser.quit()
