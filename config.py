from pathlib import Path

from config_lib import parse_config, Config

config = parse_config(str((Path(__file__).parent / 'config.ini').resolve()))

__all__ = ('config', 'Config')
