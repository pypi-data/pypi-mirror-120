import os
import uuid
from logging.config import dictConfig
from pathlib import Path
from typing import Final, List, Literal, Optional, TypedDict, cast

import attr
import tomli
import yaml

here = Path(os.path.abspath(os.path.dirname(__file__)))
DEFAULT_SETTINGS_FILE: Final[str] = "wilddog.toml"
CONFIG_FILE: List[str] = [
    "wilddog.toml",
    f"{Path.home()}/.wilddog/wilddog.toml",
    f"{here.parent.parent}/{DEFAULT_SETTINGS_FILE}",
]


class LoggingConfig(TypedDict):
    level: str
    log_file: str


class EnvironmentVars(TypedDict, total=False):
    git_home: str


class DatabaseConfig(TypedDict, total=False):
    url: str


class FlaskConfig(TypedDict):
    secret_key: str


class ServerConfig(TypedDict):
    host: str
    port: int
    scheme: Literal["https", "http"]
    threads: int


class Config(TypedDict):
    title: str
    api: FlaskConfig
    database: DatabaseConfig
    environment: EnvironmentVars
    logging: LoggingConfig
    server: ServerConfig


class WildDogConfig:
    def __init__(self, cfg: Config) -> None:
        self.load_id = str(uuid.uuid4())
        self.cfg = cfg

    @property
    def title(self) -> str:
        return self.cfg["title"]

    @property
    def database(self) -> DatabaseConfig:
        return self.cfg["database"]

    @property
    def environment(self) -> EnvironmentVars:
        return self.cfg.get("environment", {})

    @property
    def logging(self) -> LoggingConfig:
        return self.cfg["logging"]

    @property
    def flask(self) -> FlaskConfig:
        return self.cfg["api"]

    @property
    def server(self) -> ServerConfig:
        return self.cfg["server"]

    def _configure_logger(self) -> None:
        cfg = self.logging

        level = cfg["level"]
        log_file = cfg["log_file"]
        lcfg = yaml.safe_load(
            f"""
            version: 1
            formatters:
              simple:
                format: '%(asctime)s %(levelname)s [%(name)s:%(lineno)d] %(message)s'
            handlers:
              console:
                class: logging.StreamHandler
                level: {level}
                formatter: simple
                stream: ext://sys.stdout
              file:
                class: logging.handlers.RotatingFileHandler
                level: {level}
                formatter: simple
                filename: {log_file}
                maxBytes: 4096
                backupCount: 10
            loggers:
              plaster:
                level: {level}
                handlers: [console, file]
                propagate: no
            root:
              level: {level}
              handlers: [console, file]
        """
        )

        dictConfig(lcfg)

    def _configure_env(self) -> None:
        for key, val in self.environment.items():
            os.environ[f"PLASTER_{key.upper()}"] = str(val)

    def configure(self) -> None:
        self._configure_env()
        self._configure_logger()


@attr.s(auto_attribs=True)
class WildDogConfigFile:
    uri: Optional[str] = None

    @property
    def filename(self) -> str:
        if self.uri:
            return self.uri
        for p in CONFIG_FILE:
            path = Path(p)
            if not path.exists():
                continue
            return p
        raise ValueError("No settings file found")

    def load(self) -> WildDogConfig:
        with open(self.filename, "r") as f:
            raw_cfg = tomli.load(f)
            cfg = WildDogConfig(cfg=cast(Config, raw_cfg))
            cfg.configure()

            return cfg


wild_dog = WildDogConfigFile().load()
