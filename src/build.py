"""Build scripts."""

import logging
import subprocess

from src.const import (
    GENAI_BUILD_SCRIPT,
    OV_BUILD_SCRIPTS_DIR,
    OV_BUILD_SCRIPTS_PATH,
    TOKENIZERS_BUILD_SCRIPT,
)
from src.git import sync_git_repo
from src.models import BasePackageUpdateModel, OpenVINOPackageUpdateModel, OVPackageUpdateModel

logger = logging.getLogger(__name__)


def build_openvino(config: OpenVINOPackageUpdateModel) -> None:
    """Build OpenVINO."""
    if not config.Update:
        logger.info("UPDATE_OPENVINO set to 0, not building.")
        return
    logger.info("Building OpenVINO")
    update_ov_dependencies()
    sync_git_repo(config)
    if config.BuildFile and config.BuildFile.exists():
        msg = f"Using script at {config.BuildFile}"
        logger.info(msg)
        script_path = config.BuildFile
    else:
        script = OV_BUILD_SCRIPTS_PATH.get(config.BuildType)
        if script is None:
            msg = f"Cannot build script for {config.BuildType}, not yet implemented."
            raise NotImplementedError(msg)
        script_path = f"{OV_BUILD_SCRIPTS_DIR}/{script}"
    subprocess.run([script_path], check=True, shell=True)  # noqa: S602
    logger.info("Finished building OpenVINO")


def build_genai(config: OVPackageUpdateModel) -> None:
    """Build GenAI."""
    if not config.Update:
        logger.info("UPDATE_GENAI set to 0, not building.")
        return
    logger.info("Building OpenVINO-GenAI")
    sync_git_repo(config)
    subprocess.run([GENAI_BUILD_SCRIPT], check=True, shell=True)  # noqa: S602
    logger.info("Finished building OpenVINO-GenAI")


def build_tokenizers(config: BasePackageUpdateModel) -> None:
    """Build Tokenizers."""
    if not config.Update:
        logger.info("UPDATE_TOKENIZERS set to 0, not building.")
        return
    logger.info("Building Tokenizers")
    subprocess.run([TOKENIZERS_BUILD_SCRIPT], check=True, shell=True)  # noqa: S602
    logger.info("Finished building Tokenizers")


def update_ov_dependencies() -> None:
    """Update OpenVINO dependencies."""
    logger.debug("Installing system dependencies...")
    cmd = ["/openvino_src/install_build_dependencies.sh"]
    subprocess.run(cmd, check=True, shell=True)  # noqa: S602
    logger.debug("System dependencies installed.")
    logger.debug("Installing Python dependencies...")
    cmd = ["uv pip install -r /openvino_src/src/bindings/python/wheel/requirements-dev.txt"]
    subprocess.run(cmd, check=True, shell=True)  # noqa: S602
    logger.debug("Python dependencies installed.")
