import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

from core.browser_manager import Browser

browser = Browser("firefox", headless=False)
browser.go_to("https://servicos-crea-ma.sitac.com.br/index.php")
browser.type("#login", "usuario_teste")
browser.click("#enviar")
browser.quit()
