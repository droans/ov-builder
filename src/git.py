"""Scripts related to git commands over repository."""

import contextlib
import logging
import subprocess
from pathlib import Path
from typing import overload

from src.models import ConfigModel, GitRemoteModel
from src.util import OVPackageUpdateModel, create_short_uuid

logger = logging.getLogger(__name__)


def sync_git_repos(config: ConfigModel) -> None:
    """Syncs all git repos from the config at once."""
    packages = config.Packages
    logger.debug("Syncing repos....")
    logger.debug("Syncing OpenVINO repo.")
    sync_git_repo(packages.OpenVINO)
    logger.debug("Syncing GenAI repo.")
    sync_git_repo(packages.GenAI)
    logger.debug("Finished syncing repos")


def sync_git_repo(config: OVPackageUpdateModel) -> None:
    """Synchronize a git repository."""
    get_git_remote(config, create=True)
    with contextlib.suppress(BaseException):
        # Any command failure is likely due to a branch already being checked out,
        update_git_repo(config)
    if config.PullRequest:
        select_git_pr(config)
    else:
        select_git_branch(config)


def update_git_repo(config: OVPackageUpdateModel) -> None:
    """Runs git pull over a repo."""
    msg = f"Pulling repo at {config.RepoDir}"
    logger.debug(msg)
    _run_git_command("pull", config)


def select_git_branch(config: OVPackageUpdateModel) -> None:
    """Switch to the selected git branch."""
    remote = get_git_remote(config)
    msg = f"Switching branches to {config.Branch}"
    logger.debug(msg)
    if not remote:
        msg = f"Remote {config.Remote} does not exist."
        raise RuntimeError(msg)
    update_git_repo(config)
    cmd = f"checkout -q {config.Branch}"
    cmd = cmd.replace("//", "/")
    msg = f"Using command: {cmd}"
    logger.debug(msg)
    _run_git_command(cmd, config)


def select_git_pr(config: OVPackageUpdateModel) -> None:
    """Switch to the selected git PR."""
    branch_uuid = create_short_uuid()
    remote = get_git_remote(config)
    if not remote:
        msg = f"Remote {config.Remote} does not exist."
        raise RuntimeError(msg)
    msg = f"Selecting PR {config.PullRequest} (Merge: {config.UseMerged})"
    logger.debug(msg)
    base_cmd = f"fetch {remote.Name} pull/{config.PullRequest}"
    cmd = f"{base_cmd}/merge" if config.UseMerged else "/head"
    cmd += f":{branch_uuid}"
    msg = f"Using command: {cmd}"
    logger.debug(msg)
    _run_git_command(cmd, config)
    checkout_cmd = f"checkout -q {branch_uuid}"
    logger.debug("Checking out...")
    msg = f"Using command: {cmd}"
    logger.debug(msg)
    _run_git_command(checkout_cmd, config)


def add_git_remote(config: OVPackageUpdateModel) -> GitRemoteModel:
    """Add a remote to the repository."""
    remote = config.Remote
    remote_url = create_gh_remote_url(remote)
    msg = f"Adding remote for {remote_url}"
    logger.debug(msg)
    remote_uuid = create_short_uuid()
    cmd = f"remote add {remote_uuid} {remote_url}"
    msg = f"Using command: {cmd}"
    logger.debug(msg)
    _run_git_command(cmd, config)
    return GitRemoteModel(
        Name=remote_uuid,
        Address=remote_url,
        RemoteType="*",
    )


def get_git_remote(config: OVPackageUpdateModel, create: bool = False) -> GitRemoteModel | None:
    """Returns a configured git remote."""
    remotes = get_git_remotes(config.RepoDir)
    remote = [remote for remote in remotes if config.Remote in remote.Address]
    if remote:
        return remote[0]
    if create:
        add_git_remote(config)
    return get_git_remote(config)


def git_remote_exists(config: OVPackageUpdateModel) -> bool:
    """Return True if remote exists, False if it does not."""
    remotes = get_git_remotes(config.RepoDir)
    return any(config.Remote in remote.Address for remote in remotes)


def _create_git_remote_model(remote_data: str) -> GitRemoteModel:
    """Creates a remote model from a string output taken from calling `git remote -v` and splitting by line."""
    msg = f"Got remote data '{remote_data}'"
    logger.debug(msg)
    remote_name, address_type = remote_data.split("\t")
    remote_address, remote_type = address_type.split(" ")
    remote_type = remote_type.replace("(", "").replace(")", "")
    return GitRemoteModel(
        Name=remote_name,
        Address=remote_address,
        RemoteType=remote_type,
    )


def get_git_remotes(repo_directory: str | Path) -> list[GitRemoteModel]:
    """Get all git remotes."""
    if isinstance(repo_directory, Path):
        repo_directory = repo_directory.as_posix()
    cmd = "remote -v"
    result = _run_git_command(cmd, repo_directory)
    remotes = result.stdout.decode().split("\n")
    msg = f"Remotes: {result.stdout.decode()}"
    logger.debug(msg)
    return [_create_git_remote_model(remote) for remote in remotes if len(remote)]


def create_gh_remote_url(repo: str) -> str:
    """Generate the URL for a GitHub remote."""
    result = f"https://github.com/{repo}"
    return result if result.endswith(".git") else f"{result}.git"


@overload
def _run_git_command(cmd: str, config_or_repo_dir: str) -> subprocess.CompletedProcess[bytes]: ...


@overload
def _run_git_command(
    cmd: str,
    config_or_repo_dir: OVPackageUpdateModel,
) -> subprocess.CompletedProcess[bytes]: ...


def _run_git_command(
    cmd: str,
    config_or_repo_dir: OVPackageUpdateModel | str,
) -> subprocess.CompletedProcess[bytes]:
    """Run a git command in a subprocess."""
    repo_dir = (
        config_or_repo_dir.RepoDir.as_posix()
        if isinstance(config_or_repo_dir, OVPackageUpdateModel)
        else config_or_repo_dir
    )
    cmd = f"git -C {repo_dir} {cmd}"
    full_cmd = ["bash", "-c", cmd]
    msg = f"Running command {cmd}"
    logger.debug(msg)
    try:
        result = subprocess.run(full_cmd, check=True, shell=False, capture_output=True)  # noqa: S603
        msg = f"stdout: {result.stdout}"
        logger.debug(msg)
        msg = f"stderr: {result.stderr}"
        logger.debug(msg)
    except subprocess.CalledProcessError as e:
        logger.exception("Got error!")
        msg = f"stderr: {e.stderr}"
        logger.exception(msg)
        msg = f"stdout: {e.stdout}"
        logger.exception(msg)
        msg = f"output: {e.output}"
        logger.exception(msg)
        logger.exception(e.stdout)
        logger.exception(e.output)
        raise
    return result
