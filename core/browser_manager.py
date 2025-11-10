"""Wrapper simples sobre Selenium WebDriver.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import shutil
import os
import time
from typing import Optional, List

class Browser:
    def __init__(self, browser: str = "chrome", headless: bool = True, driver_path: Optional[str] = None, implicit_wait: int = 5):
        self.browser_name = browser.lower()
        self.headless = headless
        self.driver_path = driver_path
        self.implicit_wait = implicit_wait
        self.driver = self._start_driver()
        self.driver.implicitly_wait(self.implicit_wait)

    def _start_driver(self):
        options = None
        if self.browser_name == "chrome":
            from selenium.webdriver.chrome.options import Options
            options = Options()
            if self.headless:
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            if self.driver_path:
                return webdriver.Chrome(executable_path=self.driver_path, options=options)
            return webdriver.Chrome(options=options)
        elif self.browser_name == "firefox":
            from selenium.webdriver.firefox.options import Options
            options = Options()
            if self.headless:
                options.headless = True
            if self.driver_path:
                return webdriver.Firefox(executable_path=self.driver_path, options=options)
            return webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Browser '{self.browser_name}' não suportado")

    def go_to(self, url: str):
        self.driver.get(url)

    def click(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10):
        el = self.wait_for(selector, by=by, timeout=timeout)
        el.click()

    def type(self, selector: str, text: str, by: By = By.CSS_SELECTOR, timeout: int = 10, clear_first: bool = True):
        el = self.wait_for(selector, by=by, timeout=timeout)
        if clear_first:
            el.clear()
        el.send_keys(text)

    def get_text(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> str:
        el = self.wait_for(selector, by=by, timeout=timeout)
        return el.text

    def wait_for(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, selector)))
        except TimeoutException:
            raise TimeoutException(f"Elemento {selector} não localizado após {timeout} segundos")

    def extract_table(self, table_selector: str, by: By = By.CSS_SELECTOR, header: bool = True) -> List[dict]:
        """Extrai tabela HTML simples em lista de dicionários.

        Atenção: assume markup sem células mescladas.
        """
        table = self.wait_for(table_selector, by=by)
        rows = table.find_elements(By.TAG_NAME, 'tr')
        data = []
        headers = []
        if header and rows:
            # primeiro tr como header
            ths = rows[0].find_elements(By.TAG_NAME, 'th')
            if ths:
                headers = [th.text.strip() for th in ths]
                data_rows = rows[1:]
            else:
                # fallback: usar tds do primeiro row
                tds = rows[0].find_elements(By.TAG_NAME, 'td')
                headers = [f'col_{i}' for i in range(len(tds))]
                data_rows = rows
        else:
            data_rows = rows
        for r in data_rows:
            cells = r.find_elements(By.TAG_NAME, 'td')
            if not cells:
                continue
            values = [c.text.strip() for c in cells]
            row_obj = {headers[i] if i < len(headers) else f'col_{i}': values[i] for i in range(len(values))}
            data.append(row_obj)
        return data

    def screenshot(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.driver.save_screenshot(path)

    def quit(self):
        try:
            self.driver.quit()
        except Exception:
            pass