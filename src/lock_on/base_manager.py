from abc import ABC, abstractmethod
import json
from lock_on.package_models import Package, Constraint, Version


class PackageManager(ABC):
    """Interface for a toy package manager."""

    def __init__(self):
        self.requirements = self._read_requirements()
        self.index = self._read_dependencies()

    def _read_requirements(self) -> list[str]:
        """Discover requirements.txt."""
        with open("deps/requirements.txt") as f:
            return f.read().splitlines() 

    def _read_dependencies(self) -> dict[str, Package]:
        """
        Parse mock dependency graphs
        
        this imitates what we would recieve by constructing 
        dependency graphs by reading wheel metadata.
        """

        index: dict[str, Package] = {}
        
        with open('deps/dep_graph.json') as file:
            dep_graph: dict = json.load(file).get("packages")
            
            for package in dep_graph:
                pkg = Package(
                    name=package,
                    versions={}
                )
                for version in dep_graph[package]:
                    requires = dep_graph[package][version]["requires"]
                    ver = Version(
                        number=version,
                        dependencies=[Constraint.from_string(r) for r in requires]
                    )
                    pkg.versions[version] = ver
                index[package] = pkg

        return index

    @abstractmethod
    def resolve(self) -> dict:
        """Resolver implmentation"""
        return {}
