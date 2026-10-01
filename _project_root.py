import inspect
import os
import pathlib
from typing import Optional, TextIO


def _find_project_root(path: pathlib.Path) -> pathlib.Path | None:
    path = path.resolve()
    while path != path.parent:
        if "site-packages" not in path.parts and (path / "pyproject.toml").is_file():
            return path
        path = path.parent
    return None


class ProjectRoot:
    def __init__(self):
        package_root = pathlib.Path(__file__).parent
        if project_root := _find_project_root(package_root):
            self.project_root = project_root
            return
        for frame in inspect.stack()[1:]:
            caller = pathlib.Path(frame.filename)
            if "site-packages" in caller.parts:
                continue
            self.project_root = _find_project_root(caller.parent) or caller.parent
            return
        self.project_root = package_root

    def path(self, path: Optional[str] = None) -> str:
        return os.path.join(self.project_root, path or "")

    def open(self, path: str, *args, **kwargs) -> TextIO:
        return open(self.path(path), *args, **kwargs)


project_root = ProjectRoot()

__all__ = ["project_root"]
