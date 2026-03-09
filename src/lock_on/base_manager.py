import json
from abc import ABC, abstractmethod
from pathlib import Path

from lock_on.models import Constraint, Package, Version


class PackageManager(ABC):
    """Interface for a toy package manager."""

    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    def __init__(self):
        self.requirements: list[Constraint] = self._read_requirements()
        self.index: dict[str, Package] = self._read_dependencies()

    def _read_requirements(self) -> list[Constraint]:
        """Parse mock requirements.txt."""

        with Path("deps/requirements.txt").open() as file:
            return [
                Constraint.from_string(requirement)
                for requirement in file.read().splitlines()
            ]

    def _read_dependencies(self) -> dict[str, Package]:
        """
        Parse mock dependency graphs

        this imitates what we would ultimately recieve from
        constructing dependency graphs by reading wheel metadata.
        """

        index: dict[str, Package] = {}

        with Path("deps/dep_graph.json").open() as file:
            dep_graph: dict = json.load(file).get("packages")

            for package in dep_graph:
                pkg = Package(name=package, versions={})
                for version in dep_graph[package]:
                    requires = dep_graph[package][version]["requires"]
                    ver = Version(
                        number=version,
                        dependencies=[Constraint.from_string(r) for r in requires],
                    )
                    pkg.versions[version] = ver
                index[package] = pkg

        return index

    def _log(self, msg: str, colour: str) -> None:
        print(f"{colour}{msg}{self.RESET}")

    def _write_to_lock_file(self, solution: dict) -> None:
        """Write the final solution from resolver to lock file."""

        with Path("deps/lock.json").open("w") as file:
            sol_json = json.dumps(solution, indent=4)
            file.write(sol_json)

    @abstractmethod
    def resolve(self) -> None:
        """Resolver implmentation"""

        pass
