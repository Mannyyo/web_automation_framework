import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

import time
from core.browser_manager import Browser
from utils.logger import setup_logger


logger = setup_logger()

def exemplo():
    nav = Browser(browser='firefox', headless=False)
    try:
        logger.info('Acessando o site')
        nav.go_to('https://servicos-crea-ma.sitac.com.br/index.php')
        logger.info('Realizando login')
        nav.type('#login', '00000000000000')
        nav.type('#senha', 'minha_senha')
        nav.click('#enviar')
        
        time.sleep(1)
        
        logger.info('Buscando mensagem de erro')
        nav.wait_for('#error_message')
        error_message = nav.get_text('#error_message')
        logger.info(f"{error_message}")
        
        path = os.path.join(os.curdir, 'examples', 'screenshots', 'exemplo_login_sitac.png')
        nav.screenshot(path)
    finally:
        nav.quit()


if __name__ == '__main__':
    exemplo()