"""
Browser — Wrapper robusto para Selenium WebDriver
-------------------------------------------------
Inclui:
- Logging detalhado de ações e erros
- Retry automático em operações críticas
- Suporte a Chrome e Firefox
- Métodos utilitários para páginas e POM
"""

import os
import time
from typing import Optional, List, Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from core.config_manager import ConfigManager
from utils.logger import setup_logger
from utils.decorators import retry_on_fail
from utils.error_handler import capture_failures


class Browser:
    def __init__(
        self,
        browser: str = None,
        headless: bool = None,
        driver_path: Optional[str] = None,
        implicit_wait: int = None,
        explicit_timeout: int = None,
        log_level: Union[str, int] = None,
    ):
        
        cfg = ConfigManager

        self.browser_name = browser.lower() or cfg.get("BROWSER", "chrome")
        self.headless = headless if headless is not None else ctg.get("HEADLESS", True, cast=bool)
        # self.driver_path = driver_path
        self.implicit_wait = implicit_wait or cfg.get("IMPLICIT_WAIT", 5, cast=int)
        self.explicit_timeout = explicit_timeout or cfg.get("EXPLICIT_TIMEOUT", 10, cast=int)
        self.log_level = log_level or cfg.get("LOG_LEVEL", "INFO")
        
        self.logger = setup_logger("browser", level=self.log_level)

        self.logger.info(f"Iniciando navegador: {self.browser_name} (headless={self.headless})")
        self.driver = self._start_driver()
        self.driver.implicitly_wait(self.implicit_wait)
        self.logger.info("WebDriver inicializado com sucesso.")

    # ------------------------------------------------------------------
    # Inicialização do driver
    # ------------------------------------------------------------------
    def _start_driver(self):
        if self.browser_name == "chrome":
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager

            options = Options()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            driver_path = ChromeDriverManager().install()
            self.logger.info(f"ChromeDriver obtido em: {driver_path}")
            
            service = ChromeService(driver_path)
            return webdriver.Chrome(service=service, options=options)

        elif self.browser_name == "firefox":
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager

            options = Options()
            options.headless = self.headless
            
            driver_path = GeckoDriverManager().install()
            self.logger.info(f"GeckoDriver obtido em: {driver_path}")
            
            service = FirefoxService(driver_path)
            return webdriver.Firefox(service=service, options=options)

        else:
            raise ValueError(f"Browser '{self.browser_name}' não suportado.")

    # ------------------------------------------------------------------
    # Navegação e Esperas
    # ------------------------------------------------------------------
    def go_to(self, url: str):
        self.logger.info(f"Acessando URL: {url}")
        self.driver.get(url)

    @capture_failures
    @retry_on_fail(retries=3, delay=1.5)
    def wait_for(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = None):
        self.logger.debug(f"Aguardando elemento: {selector}")
        timeout = timeout or self.explicit_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, selector)))
            self.logger.debug(f"Elemento localizado: {selector}")
            return element
        except TimeoutException as e:
            self.logger.error(f"Timeout: elemento '{selector}' não encontrado em {timeout}s.")
            raise e

    # --------------------------------------------------------------
    # CONTROLE DE ABAS E JANELAS
    # --------------------------------------------------------------
    def new_tab(self, url: str = None):
        """Abre uma nova aba e navega opcionalmente para uma URL."""
        self.logger.info("Abrindo nova aba...")
        self.driver.execute_script("window.open('');")
        self.switch_to_tab(self.tabs_count() - 1)
        if url:
            self.go_to(url)

    def tabs_count(self) -> int:
        return len(self.driver.window_handles)

    @capture_failures
    def switch_to_tab(self, index: int):
        """Troca para a aba pelo índice."""
        handles = self.driver.window_handles
        if index < 0 or index >= len(handles):
            raise IndexError(f"Índice de aba inválido: {index}")

        self.logger.info(f"Alterando para aba {index}")
        self.driver.switch_to.window(handles[index])

    def current_tab(self) -> int:
        """Retorna o índice da aba atual."""
        return self.driver.window_handles.index(self.driver.current_window_handle)

    def close_tab(self):
        """Fecha a aba atual e muda para a última."""
        self.logger.info("Fechando aba atual")
        self.driver.close()
        if self.tabs_count() > 0:
            self.switch_to_tab(self.tabs_count() - 1)
    
    def close_all_other_tabs(self):
        """Fecha todas as abas exceto a aba atual."""
        current_handle = self.driver.current_window_handle
        all_handles = self.driver.window_handles

        self.logger.info(f"Fechando demais abas")
        for handle in all_handles:
            if handle != current_handle:
                self.driver.switch_to.window(handle)
                self.driver.close()

        self.logger.info("Retornando à aba atual")
        self.driver.switch_to.window(current_handle)

    # --------------------------------------------------------------
    # CONTROLE DE FRAMES
    # --------------------------------------------------------------
    @capture_failures
    def switch_to_frame(self, selector: str, by=By.CSS_SELECTOR, timeout: int = None):
        """Troca para um frame localizado por seletor CSS."""
        self.logger.info(f"Alternando para frame: {selector}")
        timeout = timeout or self.explicit_timeout
        el = self.wait_for(selector, by=by, timeout=timeout)
        self.driver.switch_to.frame(el)

    def switch_to_frame_by_index(self, index: int):
        """Troca para um frame pelo índice numérico."""
        self.logger.info(f"Alternando para frame índice: {index}")
        self.driver.switch_to.frame(index)

    def switch_to_default(self):
        """Sai do frame e volta para o conteúdo principal."""
        self.logger.info("Retornando ao conteúdo principal (default content)")
        self.driver.switch_to.default_content()

    # ------------------------------------------------------------------
    # Ações de interação
    # ------------------------------------------------------------------
    @capture_failures
    @retry_on_fail(retries=3, delay=2.0)
    def click(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = None):
        self.logger.debug(f"Tentando clicar em: {selector}")
        timeout = timeout or self.explicit_timeout
        element = self.wait_for(selector, by=by, timeout=timeout)
        try:
            element.click()
            self.logger.info(f"Clique realizado com sucesso em '{selector}'")
        except (ElementClickInterceptedException, StaleElementReferenceException) as e:
            self.logger.warning(f"Falha ao clicar ({e.__class__.__name__}), tentando novamente...")
            raise e

    @capture_failures
    @retry_on_fail(retries=3, delay=1.5)
    def type(
        self,
        selector: str,
        text: str,
        by: By = By.CSS_SELECTOR,
        timeout: int = None,
        clear_first: bool = True,
    ):
        self.logger.debug(f"Digitando em {selector}: '{text}'")
        timeout = timeout or self.explicit_timeout
        element = self.wait_for(selector, by=by, timeout=timeout)
        try:
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Texto '{text}' inserido com sucesso em '{selector}'")
        except StaleElementReferenceException as e:
            self.logger.warning(f"Falha ao digitar ({e.__class__.__name__}), tentando novamente...")
            raise e

    @capture_failures
    def get_text(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = None) -> str:
        timeout = timeout or self.explicit_timeout
        element = self.wait_for(selector, by=by, timeout=timeout)
        text = element.text
        self.logger.debug(f"Texto obtido de '{selector}': {text[:50]}")
        return text

    # --------------------------------------------------------------
    # INTERAÇÕES AVANÇADAS
    # --------------------------------------------------------------
    def action_chain(self) -> ActionChains:
        """Retorna um objeto ActionChains para construção manual."""
        self.logger.debug("Construindo ActionChain manual.")
        return ActionChains(self.driver)

    def move_to(self, selector: str, by=By.CSS_SELECTOR, timeout: int = None):
        """Move o mouse até o elemento."""
        self.logger.info(f"Movendo mouse para {selector}")
        timeout = timeout or self.explicit_timeout
        el = self.wait_for(selector, by=by, timeout=timeout)
        ActionChains(self.driver).move_to_element(el).perform()

    def hover(self, selector: str, by=By.CSS_SELECTOR, timeout: int = None):
        """Efetua um hover sobre o elemento."""
        self.logger.info(f"Hover em {selector}")
        timeout = timeout or self.explicit_timeout
        el = self.wait_for(selector, by=by, timeout=timeout)
        ActionChains(self.driver).move_to_element(el).perform()

    def double_click(self, selector: str, by=By.CSS_SELECTOR, timeout: int = None):
        """Dá um double-click no elemento."""
        self.logger.info(f"Double-click em {selector}")
        timeout = timeout or self.explicit_timeout
        el = self.wait_for(selector, by=by, timeout=timeout)
        ActionChains(self.driver).double_click(el).perform()

    def right_click(self, selector: str, by=By.CSS_SELECTOR, timeout: int = None):
        """Clique com botão direito."""
        self.logger.info(f"Right-click em {selector}")
        timeout = timeout or self.explicit_timeout
        el = self.wait_for(selector, by=by, timeout=timeout)
        ActionChains(self.driver).context_click(el).perform()

    def click_and_hold(self, selector: str, by=By.CSS_SELECTOR, timeout: int = None):
        """Clique e segura o botão do mouse."""
        self.logger.info(f"Click-and-hold em {selector}")
        timeout = timeout or self.explicit_timeout
        el = self.wait_for(selector, by=by, timeout=timeout)
        ActionChains(self.driver).click_and_hold(el).perform()

    def release(self):
        """Solta o botão do mouse."""
        self.logger.info("Soltando click (release)")
        ActionChains(self.driver).release().perform()

    # --------------------------------------------------------------
    # Drag & drop
    # --------------------------------------------------------------
    def drag_and_drop(self, source_selector: str, target_selector: str, by=By.CSS_SELECTOR, timeout: int = None):
        """Arrasta um elemento e solta em outro."""
        self.logger.info(f"Drag and drop: {source_selector} ➜ {target_selector}")
        timeout = timeout or self.explicit_timeout

        source = self.wait_for(source_selector, by=by, timeout=timeout)
        target = self.wait_for(target_selector, by=by, timeout=timeout)

        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def drag_and_drop_offset(self, selector: str, x: int, y: int, by=By.CSS_SELECTOR, timeout: int = None):
        """Arrasta elemento por deslocamento (x, y)."""
        self.logger.info(f"Drag by offset: {selector} ➜ ({x}, {y})")
        timeout = timeout or self.explicit_timeout

        element = self.wait_for(selector, by=by, timeout=timeout)
        ActionChains(self.driver).drag_and_drop_by_offset(element, x, y).perform()

    # --------------------------------------------------------------
    # TECLADO AVANÇADO
    # --------------------------------------------------------------
    def press_key(self, key: str):
        """Pressiona uma tecla única (ex: Keys.ENTER)."""
        self.logger.info(f"Pressionando tecla: {key}")
        ActionChains(self.driver).send_keys(key).perform()

    def key_down(self, key: str):
        """Mantém tecla pressionada."""
        self.logger.info(f"Key down: {key}")
        ActionChains(self.driver).key_down(key).perform()

    def key_up(self, key: str):
        """Solta tecla pressionada."""
        self.logger.info(f"Key up: {key}")
        ActionChains(self.driver).key_up(key).perform()

    # --------------------------------------------------------------
    # SCROLL AVANÇADO
    # --------------------------------------------------------------
    def scroll_by(self, x: int, y: int):
        """Scroll absoluto em coordenadas (x, y)."""
        self.logger.info(f"Scrolling by ({x}, {y})")
        self.driver.execute_script(f"window.scrollBy({x}, {y});")

    def scroll_to_element(self, selector: str, by=By.CSS_SELECTOR, timeout: int = None):
        """Scroll até um elemento específico (scrollIntoView)."""
        self.logger.info(f"Scroll até elemento: {selector}")
        timeout = timeout or self.explicit_timeout
        el = self.wait_for(selector, by=by, timeout=timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", el)

    # ------------------------------------------------------------------
    # Extração de dados
    # ------------------------------------------------------------------
    @capture_failures
    @retry_on_fail(retries=2, delay=2.0)
    def extract_table(
        self, table_selector: str, by: By = By.CSS_SELECTOR, header: bool = True
    ) -> List[dict]:
        """Extrai tabela HTML simples em lista de dicionários."""
        self.logger.info(f"Extraindo tabela: {table_selector}")
        table = self.wait_for(table_selector, by=by)
        rows = table.find_elements(By.TAG_NAME, "tr")
        data = []
        headers = []

        if header and rows:
            ths = rows[0].find_elements(By.TAG_NAME, "th")
            if ths:
                headers = [th.text.strip() for th in ths]
                data_rows = rows[1:]
            else:
                tds = rows[0].find_elements(By.TAG_NAME, "td")
                headers = [f"col_{i}" for i in range(len(tds))]
                data_rows = rows
        else:
            data_rows = rows

        for r in data_rows:
            cells = r.find_elements(By.TAG_NAME, "td")
            if not cells:
                continue
            values = [c.text.strip() for c in cells]
            row_obj = {
                headers[i] if i < len(headers) else f"col_{i}": values[i]
                for i in range(len(values))
            }
            data.append(row_obj)

        self.logger.info(f"Tabela extraída com {len(data)} linhas.")
        return data

    # --------------------------------------------------------------
    # CONTROLE DE ALERTS
    # --------------------------------------------------------------
    def alert_accept(self):
        """Aceita o alert."""
        self.logger.info("Aceitando alert...")
        alert = self.driver.switch_to.alert
        alert.accept()

    def alert_dismiss(self):
        """Cancela o alert."""
        self.logger.info("Cancelando alert...")
        alert = self.driver.switch_to.alert
        alert.dismiss()

    def alert_text(self) -> str:
        """Retorna o texto do alert."""
        alert = self.driver.switch_to.alert
        text = alert.text
        self.logger.info(f"Texto do alert: {text}")
        return text

    # --------------------------------------------------------------
    # CAPTURA DE FALHAS
    # --------------------------------------------------------------
    def capture_evidence(self, name: str):
        folder = "logs/errors"
        os.makedirs(folder, exist_ok=True)

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        base = f"{timestamp}_{name}"

        screenshot_path = os.path.join(folder, base + ".png")
        html_path = os.path.join(folder, base + ".html")

        self.driver.save_screenshot(screenshot_path)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

        self.logger.info(f"Evidências salvas: {screenshot_path}, {html_path}")

    # --------------------------------------------------------------
    # UTILITÁRIOS AVANÇADOS
    # --------------------------------------------------------------
    @capture_failures
    def execute_script(self, script: str, *args):
        """Executa JavaScript no navegador."""
        self.logger.debug(f"Executando JS: {script[:60]}...")
        return self.driver.execute_script(script, *args)

    def scroll_to(self, target):
        """Rola a página até um seletor CSS ou WebElement."""
        if isinstance(target, str):
            el = self.wait_for(target)
        else:
            el = target

        self.logger.info(f"Rolando até o elemento: {el}")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)

    # ------------------------------------------------------------------
    # Utilitários
    # ------------------------------------------------------------------
    def screenshot(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.driver.save_screenshot(path)
        self.logger.info(f"Screenshot salva em: {path}")

    def quit(self):
        self.logger.info("Encerrando navegador...")
        try:
            self.driver.quit()
            self.logger.info("Navegador fechado com sucesso.")
        except Exception as e:
            self.logger.warning(f"Falha ao encerrar o navegador: {e}")
