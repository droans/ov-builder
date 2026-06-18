"""Utility functions."""

import logging
import os
import uuid
from datetime import datetime
from pathlib import Path

from src.const import (
    DEFAULT_BRANCHES,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_REMOTES,
    ENV_GENAI,
    ENV_GIT_BRANCH_SUFFIX,
    ENV_GIT_PR_SUFFIX,
    ENV_GIT_PR_USED_MERGED_SUFFIX,
    ENV_GIT_REMOTE_SUFFIX,
    ENV_OUTPUT_DIR,
    ENV_OV,
    ENV_OV_BUILD_FILE,
    ENV_OV_BUILD_TYPE,
    ENV_SAVE_UPDATE_CONFIG,
    ENV_TOKENIZERS,
    ENV_UPDATE_PREFIX,
    ENV_USE_DATED_FOLDERS,
    ENV_WHEEL_DIR,
    REPO_DIRECTORIES,
    UPDATE_CONFIG_FILE_NAME,
    PackageType,
)
from src.models import (
    BasePackageUpdateModel,
    ConfigModel,
    ConfigOptions,
    OpenVINOPackageUpdateModel,
    OVPackageUpdateModel,
    UpdateConfigModel,
)

logger = logging.getLogger(__name__)


def _get_ov_package_config_kwargs(base_model: OVPackageUpdateModel) -> OpenVINOPackageUpdateModel:
    """Retrieves the specific environs for OpenVINO and returns them as kwargs."""
    build_type = os.getenv(ENV_OV_BUILD_TYPE, "OCL")
    build_file = os.getenv(ENV_OV_BUILD_FILE)

    kwargs = {"BuildFile": Path(build_file)} if build_file else {"BuildType": build_type}
    return OpenVINOPackageUpdateModel(
        **base_model.model_dump(),
        **kwargs,
    )


def build_ov_or_genai_config(package_name: PackageType) -> OVPackageUpdateModel:
    """Builds the config for OpenVINO and GenAI."""
    update_key = f"{ENV_UPDATE_PREFIX}{package_name}"
    remote_key = f"{package_name}{ENV_GIT_REMOTE_SUFFIX}"
    branch_key = f"{package_name}{ENV_GIT_BRANCH_SUFFIX}"
    pr_key = f"{package_name}{ENV_GIT_PR_SUFFIX}"
    pr_use_merged_key = f"{package_name}{ENV_GIT_PR_USED_MERGED_SUFFIX}"

    default_remote = DEFAULT_REMOTES[package_name]
    default_branch = DEFAULT_BRANCHES[package_name]

    update = os.getenv(update_key) != "0"
    remote = os.getenv(remote_key) or default_remote
    branch = os.getenv(branch_key) or default_branch
    pr_val = os.getenv(pr_key)
    pr = int(pr_val) if pr_val else None
    pr_use_merged = bool(os.getenv(pr_use_merged_key)) or None
    repo_dir = Path(REPO_DIRECTORIES[package_name])

    model = OVPackageUpdateModel(
        Update=update,
        Remote=remote,
        Branch=branch,
        PullRequest=pr,
        UseMerged=pr_use_merged,
        RepoDir=repo_dir,
    )
    return model if package_name != ENV_OV else _get_ov_package_config_kwargs(model)


def build_tokenizers_config() -> BasePackageUpdateModel:
    """Build Tokenizers config."""
    update_key = f"{ENV_UPDATE_PREFIX}{ENV_TOKENIZERS}"
    update = os.getenv(update_key) != "0"
    return BasePackageUpdateModel(Update=update)


def build_package_config(package_name: PackageType) -> BasePackageUpdateModel:
    """Build the configuration for a single package."""
    if package_name == ENV_TOKENIZERS:
        return build_tokenizers_config()
    return build_ov_or_genai_config(package_name)


def build_packages_config() -> UpdateConfigModel:
    """Build the configuration for all packages."""
    return UpdateConfigModel(
        OpenVINO=build_package_config(ENV_OV),  # ty:ignore[invalid-argument-type]
        GenAI=build_package_config(ENV_GENAI),  # ty:ignore[invalid-argument-type]
        Tokenizers=build_package_config(ENV_TOKENIZERS),
    )


def build_options_config() -> ConfigOptions:
    """Build the model for config options."""
    output_dir = Path(os.getenv(ENV_OUTPUT_DIR) or DEFAULT_OUTPUT_DIR)
    use_dated_folders = os.getenv(ENV_USE_DATED_FOLDERS) != "0"
    save_update_config = os.getenv(ENV_SAVE_UPDATE_CONFIG) != "0"

    return ConfigOptions(
        OutputDirectory=output_dir,
        UseDatedFolders=use_dated_folders,
        SaveUpdateConfig=save_update_config,
    )


def build_config_from_env() -> ConfigModel:
    """Build OV configuration from the environment variables."""
    return ConfigModel(
        Options=build_options_config(),
        Packages=build_packages_config(),
    )


def create_short_uuid() -> str:
    """Creates an eight-digit long UUID."""
    return str(uuid.uuid4())[:8]


def set_script_envs(config: ConfigModel) -> None:
    """Sets configuration options as environmental variables for the scripts."""
    options = config.Options
    out_dir = options.OutputDirectory
    if options.UseDatedFolders:
        dt_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        out_dir = Path(out_dir, dt_str)
        out_dir.mkdir()
    os.environ[ENV_WHEEL_DIR] = out_dir.as_posix()


def export_environ(config: ConfigModel) -> None:
    """Exports the environment variables to a JSON file."""
    save_dir = os.environ[ENV_WHEEL_DIR]
    path = Path(save_dir, UPDATE_CONFIG_FILE_NAME)
    with open(path, "w") as f:
        f.write(config.model_dump_json())
