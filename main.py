"""Main module."""

import logging

from src.build import build_genai, build_openvino, build_tokenizers
from src.util import build_config_from_env, set_logging, set_script_envs

# Set initial config before logger has loaded
logger = logging.getLogger(__name__)
log_fmt = "%(asctime)s | %(levelname)s | %(message)s"
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(log_fmt))
logging.basicConfig(
    format=log_fmt,
    level=logging.DEBUG,
    handlers=[handler],
)


def main() -> None:
    """Build updated packages for OpenVINO."""
    logger.info("OpenVINO Package Builder starting.")
    logger.info("Loading config...")
    config = build_config_from_env()
    logger.info("Got config:")
    logger.debug(config)
    logger.debug("Setting script envs...")
    set_script_envs(config)
    logger.debug("Initializing logger settings...")
    set_logging()
    logger.debug("Initializing Logger settings initialized...")
    logger.debug("Set script envs.")
    build_openvino(config.Packages.OpenVINO)
    build_tokenizers(config.Packages.Tokenizers)
    build_genai(config.Packages.GenAI)


if __name__ == "__main__":
    print("Starting OpenVINO Package Builder...")  # noqa: T201
    main()
    print("Finished OpenVINO Package Builder.")  # noqa: T201
