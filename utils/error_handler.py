import os
import time
import functools
import logging

logger = logging.getLogger("browser")


def capture_failures(func):
    """Decorator que captura screenshots + HTML quando há falha no Browser."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)

        except Exception as e:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            method = func.__name__
            folder = "logs/errors"
            os.makedirs(folder, exist_ok=True)

            # gerar nomes de arquivo
            base = f"{timestamp}_{method}"
            screenshot_path = os.path.join(folder, base + ".png")
            html_path = os.path.join(folder, base + ".html")

            # salvar screenshot
            try:
                self.driver.save_screenshot(screenshot_path)
                logger.error(f"[ERROR] Screenshot salva: {screenshot_path}")
            except Exception as ss_err:
                logger.error(f"[ERROR] Falha ao salvar screenshot: {ss_err}")

            # salvar HTML dump
            try:
                html = self.driver.page_source
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html)
                logger.error(f"[ERROR] HTML dump salvo: {html_path}")
            except Exception as html_err:
                logger.error(f"[ERROR] Falha ao salvar HTML dump: {html_err}")

            # logar exceção original
            logger.exception(f"Exceção capturada em {method}: {e}")

            # re-levantar exceção para retry ou fluxo normal
            raise e

    return wrapper
