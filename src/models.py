"""Models used by project."""

from pydantic import BaseModel, DirectoryPath, FilePath

from src.const import BuildTypes


class BasePackageUpdateModel(BaseModel):
    """Model for package update configurations."""

    Update: bool


class OVPackageUpdateModel(BasePackageUpdateModel):
    """Model for package update configurations."""

    Remote: str
    Branch: str
    PullRequest: int | None = None
    UseMerged: bool | None = None
    RepoDir: DirectoryPath


class OpenVINOPackageUpdateModel(OVPackageUpdateModel):
    """Model for OpenVINO update configuration."""

    BuildType: BuildTypes | None = None
    BuildFile: FilePath | None = None


class ConfigOptions(BaseModel):
    """Model for configuration options."""

    OutputDirectory: DirectoryPath
    UseDatedFolders: bool
    SaveUpdateConfig: bool


class UpdateConfigModel(BaseModel):
    """Model for update configurations."""

    OpenVINO: OpenVINOPackageUpdateModel
    GenAI: OVPackageUpdateModel
    Tokenizers: BasePackageUpdateModel


class ConfigModel(BaseModel):
    """Model for run configuration."""

    Options: ConfigOptions
    Packages: UpdateConfigModel


class GitRemoteModel(BaseModel):
    """Model for a single git remote listing."""

    Name: str
    Address: str
    RemoteType: str
