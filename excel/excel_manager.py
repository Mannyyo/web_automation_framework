"""Manager simples para leitura e escrita Excel usando pandas/openpyxl."""
import pandas as pd
from typing import List, Dict, Optional

class ExcelManager:
    @staticmethod
    def write(path: str, data: List[Dict], sheet_name: str = 'Sheet1', index: bool = False):
        df = pd.DataFrame(data)
        with pd.ExcelWriter(path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)

    @staticmethod
    def append(path: str, data: List[Dict], sheet_name: str = 'Sheet1', index: bool = False):
        # lê se existe, concatena e regrava
        try:
            existing = pd.read_excel(path, sheet_name=sheet_name)
            df_new = pd.DataFrame(data)
            out = pd.concat([existing, df_new], ignore_index=True)
        except Exception:
            out = pd.DataFrame(data)
        with pd.ExcelWriter(path, engine='openpyxl', mode='w') as writer:
            out.to_excel(writer, sheet_name=sheet_name, index=index)

    @staticmethod
    def read(path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        return pd.read_excel(path, sheet_name=sheet_name)