import os
from pathlib import Path


class Configs:

    def __init__(self):
        try:
            self.cache_dir = os.environ['COURT_SCRAPER_DIR']
        except KeyError:
            self.cache_dir = str(Path(os.path.expanduser('~')).joinpath('.court-scraper'))
        self.config_file_path = str(Path(self.cache_dir).joinpath('config.yaml'))
