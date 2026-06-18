"""Constants."""

from typing import Literal

BuildTypes = Literal[
    "ocl",
    "ocl-debug",
    "ze",
    "ze-debug",
    "sycl",
    "sycl-debug",
]


PackageType = Literal[
    "OPENVINO",
    "GENAI",
    "TOKENIZERS",
]

ENV_OV: PackageType = "OPENVINO"
ENV_GENAI: PackageType = "GENAI"
ENV_TOKENIZERS: PackageType = "TOKENIZERS"

ENV_UPDATE_PREFIX = "UPDATE_"
ENV_GIT_REMOTE_SUFFIX = "_GIT_REMOTE"
ENV_GIT_BRANCH_SUFFIX = "_GIT_BRANCH"
ENV_GIT_PR_SUFFIX = "_GIT_PR"
ENV_GIT_PR_USED_MERGED_SUFFIX = "_GIT_PR_USE_MERGED"
ENV_OV_BUILD_TYPE = "OPENVINO_BUILD_TYPE"
ENV_OV_BUILD_FILE = "OPENVINO_BUILD_FILE"

ENV_OUTPUT_DIR = "OUTPUT_DIR"
ENV_USE_DATED_FOLDERS = "USE_DATED_FOLDERS"
ENV_SAVE_UPDATE_CONFIG = "SAVE_UPDATE_CONFIG"

DEFAULT_OUTPUT_DIR = "/output"
DEFAULT_USE_DATED_FOLDERS = True
DEFAULT_SAVE_UPDATE_CONFIG = True
UPDATE_CONFIG_FILE_NAME = "config.json"

DEFAULT_REMOTES: dict[PackageType, str] = {
    ENV_OV: "openvinotoolkit/openvino",
    ENV_GENAI: "openvinotoolkit/openvino.genai",
}

DEFAULT_BRANCHES: dict[PackageType, str] = {
    ENV_OV: "master",
    ENV_GENAI: "master",
}

REPO_DIRECTORIES: dict[PackageType, str] = {
    ENV_OV: "/openvino_src",
    ENV_GENAI: "/genai_src",
}

ENV_WHEEL_DIR = "WHEEL_DIR"

OV_BUILD_SCRIPTS_DIR = "/build_scripts/openvino"
OV_BUILD_SCRIPTS_PATH: dict[BuildTypes, str | None] = {
    "ocl": "ocl/build.sh",
    "ze": "ze/build.sh",
    "sycl": None,
    "ocl-debug": "ocl/build-debug.sh",
    "ze-debug": "ze/build-debug.sh",
    "sycl-debug": None,
}
GENAI_BUILD_SCRIPT = "/build_scripts/genai/build.sh"
TOKENIZERS_BUILD_SCRIPT = "/build_scripts/tokenizers/build.sh"
