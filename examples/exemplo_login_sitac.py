import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

import time
from core.browser_manager import Browser


def exemplo():
    nav = Browser(browser='firefox', headless=False)
    try:
        nav.go_to('https://servicos-crea-ma.sitac.com.br/index.php')
        nav.type('#login', '00000000000000')
        nav.type('#senha', 'minha_senha')
        nav.click('#enviar')
        
        time.sleep(1)
        
        nav.wait_for('#error_message')
        error_message = nav.get_text('#error_message')
        print(error_message)
        
        path = os.path.join(os.curdir, 'examples', 'screenshots', 'exemplo_login_sitac.png')
        nav.screenshot(path)
    finally:
        nav.quit()


if __name__ == '__main__':
    exemplo()