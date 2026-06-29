"""Main module."""

import logging

from src.build import build_genai, build_openvino, build_tokenizers
from src.git import sync_git_repos
from src.util import build_config_from_env, export_config, set_logging, set_script_envs

logger = logging.getLogger(__name__)


def main() -> None:
    """Build updated packages for OpenVINO."""
    logger.info("OpenVINO Package Builder starting.")
    logger.info("Loading config...")
    config = build_config_from_env()
    logger.debug("Got config:")
    logger.debug(config)
    logger.info("Setting script envs...")
    set_script_envs(config)
    logger.debug("Set script envs.")
    if config.Options.SaveUpdateConfig:
        export_config(config)
    logger.info("Initializing logger settings...")
    set_logging()
    logger.debug("Initializing Logger settings initialized...")
    sync_git_repos(config)
    build_openvino(config.Packages.OpenVINO)
    build_tokenizers(config.Packages.Tokenizers)
    build_genai(config.Packages.GenAI)


if __name__ == "__main__":
    print("Starting OpenVINO Package Builder...")  # noqa: T201
    main()
    print("Finished OpenVINO Package Builder.")  # noqa: T201
