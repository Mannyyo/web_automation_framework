import os
import yaml
from dotenv import load_dotenv

class ConfigManager:
    _config_cache = {}

    @classmethod
    def load(cls):
        """Carrega configurações de .env e YAML apenas uma vez."""
        if cls._config_cache:
            return cls._config_cache

        # → Carregar .env
        load_dotenv()

        config = {}

        # → Carregar config.yaml (opcional)
        yaml_path = os.path.join("config", "config.yaml")
        if os.path.exists(yaml_path):
            with open(yaml_path, "r", encoding="utf-8") as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    config.update(yaml_config)

        # → Carregar variáveis de ambiente (sobrescreve YAML)
        for key, value in os.environ.items():
            config[key] = value

        cls._config_cache = config
        return config

    @classmethod
    def get(cls, key: str, default=None, cast=str):
        config = cls.load()
        value = config.get(key, default)
        if value is None:
            return default
        try:
            return cast(value)
        except:
            return value
