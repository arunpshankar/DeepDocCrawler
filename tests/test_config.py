from src.config.logging import setup_logger
from src.config.setup import load_config

logger = setup_logger()

config = load_config('./config/config.yml')
logger.info(config)