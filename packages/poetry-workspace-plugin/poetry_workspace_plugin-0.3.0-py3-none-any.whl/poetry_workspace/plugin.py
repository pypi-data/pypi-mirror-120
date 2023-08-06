from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

from cleo.events.console_events import COMMAND
from poetry.console.commands.installer_command import EnvCommand, InstallerCommand
from poetry.core.factory import Factory as BaseFactory
from poetry.core.pyproject.toml import PyProjectTOML
from poetry.core.version.pep440.version import PEP440Version
from poetry.factory import Factory
from poetry.plugins import ApplicationPlugin
from poetry.poetry import Poetry
from poetry.utils.env import EnvManager, SystemEnv, VirtualEnv

from poetry_workspace.commands import loader
from poetry_workspace.commands.workspace.workspace import WorkspaceCommand
from poetry_workspace.workspace import Workspace

if TYPE_CHECKING:
    from cleo.events.console_command_event import ConsoleCommandEvent
    from cleo.events.event_dispatcher import EventDispatcher
    from cleo.io.io import IO
    from poetry.console.application import Application


class WorkspacePlugin(ApplicationPlugin):
    def activate(self, application: "Application") -> None:
        loader.register_commands(application.command_loader)

        dispatcher = application.event_dispatcher
        dispatcher.add_listener(COMMAND, self.on_command, priority=1000)

    def on_command(self, event: "ConsoleCommandEvent", _event_name: str, _dispatcher: "EventDispatcher") -> None:
        command = event.command

        self.monkeypatch_version_parser()

        self._workspace = find_workspace(command.application, event.io)
        if self._workspace is None:
            return

        if isinstance(command, EnvCommand):
            self.monkeypatch_env_manager()

        if isinstance(command, InstallerCommand):
            self.set_installer_poetry(command, event.io)

        if isinstance(command, WorkspaceCommand):
            command.set_workspace(self._workspace)

    def set_installer_poetry(self, command: InstallerCommand, io: "IO") -> None:
        poetry = Poetry(
            file=BaseFactory.locate(Path.cwd()),
            local_config=self._workspace.poetry.local_config,
            package=self._workspace.poetry.package,
            locker=self._workspace.poetry.locker,
            config=self._workspace.poetry.config,
        )
        Factory().configure_sources(
            poetry,
            poetry.local_config.get("source", []),
            self._workspace.poetry.config,
            io,
        )
        command.set_poetry(poetry)

    def monkeypatch_env_manager(self) -> None:
        workspace_poetry = self._workspace.poetry
        original_method = EnvManager.create_venv

        def create_venv(self, *args, **kwargs) -> Union["SystemEnv", "VirtualEnv"]:
            # Set env manager's Poetry instance to the workspace Poetry instance
            # so that it creates and uses a workspace level virtualenv.
            self._poetry = workspace_poetry
            return original_method(self, *args, **kwargs)

        EnvManager.create_venv = create_venv

    def monkeypatch_version_parser(self) -> None:
        """
        Workaround for https://github.com/python-poetry/poetry/issues/4176.
        """
        original_method = PEP440Version.parse

        def parse(cls, value: str):
            value = value.rstrip(".")
            return original_method.__func__(cls, value)

        PEP440Version.parse = classmethod(parse)


def find_workspace(application: "Application", io: "IO") -> Optional[Workspace]:
    cwd = Path.cwd()
    for dir_path in [cwd] + list(cwd.parents):
        pyproject = PyProjectTOML(dir_path / "pyproject.toml")
        if not is_workspace_pyproject(pyproject):
            continue

        workspace = Workspace(pyproject, io)
        if workspace.poetry.file.path == application.poetry.file.path:
            # Currently in workspace's root project tree.
            return workspace

        for project in workspace.projects:
            if project.file.path == application.poetry.file.path:
                # Currently in a workspace project's tree.
                return workspace


def is_workspace_pyproject(pyproject: "PyProjectTOML") -> bool:
    return pyproject.file.exists() and bool(pyproject.data.get("tool", {}).get("poetry_workspace"))
