import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

import time
from core.browser_manager import Browser
from excel.excel_manager import ExcelManager
from utils.logger import setup_logger


logger = setup_logger()

def exemplo():
    nav = Browser(browser='firefox', headless=False)
    try:
        # Login no SITAC
        nav.go_to('https://crea-ma.sitac.com.br/app/view/pages/login/login.php#!')
        input('Insira usuário e senha manualmente')
        nav.wait_for('#welcome_avatar')
        
        time.sleep(1)
        
        # Fechar janela de notícias
        # nav.click('.iziModal-button')
        
        # Navegar até a tabela
        nav.click('#conteudo > div.cad_conteudo > div:nth-child(5)')
        time.sleep(1)
        nav.click('#mostrarProtocolosAReceber')
        time.sleep(1)
        nav.click('#mostrarProtocoloSetorFilial1')
        time.sleep(1)
        nav.click('#Paginator_ProtocolosSetorFilial2144 > label:nth-child(1) > a:nth-child(1)')
        
        # Extrair tabela
        data = nav.extract_table('.display')
        if data:
            path = os.path.join(os.curdir, 'examples', 'screenshots', 'saida.xlsx')
            ExcelManager.write(path, data, sheet_name='Resultados')
            logger.info(f'Dados gravados em {path}')
    finally:
        nav.quit()


if __name__ == "__main__":
    exemplo()