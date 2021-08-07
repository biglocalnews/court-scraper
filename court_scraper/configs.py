import os
import yaml
from pathlib import Path

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class ConfigurationError(Exception):
    pass


class Configs:

    def __init__(self):
        try:
            self.cache_dir = os.environ['COURT_SCRAPER_DIR']
        except KeyError:
            self.cache_dir = str(
                Path(os.path.expanduser('~'))
                .joinpath('.court-scraper')
            )
        self.config_file_path = str(
            Path(self.cache_dir)
            .joinpath('config.yaml')
        )
        self.db_path = str(
            Path(self.cache_dir)
            .joinpath('cases.db')
        )

    @property
    def captcha_service_api_key(self):
        with open(self.config_file_path, 'r') as fh:
            configs = yaml.load(fh, Loader=Loader)
            try:
                return configs['captcha_service_api_key']
            except KeyError:
                msg = f"Set captcha_service_api_key in {self.config_file_path}"
                raise ConfigurationError(msg)
