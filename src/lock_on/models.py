import re
from dataclasses import dataclass


@dataclass
class Constraint:
    """Singular package specifc constraint."""

    package_name: str
    operator: str
    version: str

    @classmethod
    def from_string(cls, constraint: str) -> Constraint:

        match = re.match(pattern=r"([a-z-]+)([><=!]+)([\d.]+)", string=constraint)

        if match is not None:
            name, op, ver = match.groups()
            return cls(package_name=name, operator=op, version=ver)
        raise ValueError("invalid contraint in graph")

    def is_satisfied_by(self, candidate: str) -> bool:
        candidate_ver = tuple(int(x) for x in candidate.split("."))
        constraint_ver = tuple(int(x) for x in self.version.split("."))

        match self.operator:
            case ">=":
                return candidate_ver >= constraint_ver
            case "<=":
                return candidate_ver <= constraint_ver
            case ">":
                return candidate_ver > constraint_ver
            case "<":
                return candidate_ver < constraint_ver
            case "==":
                return candidate_ver == constraint_ver
            case "!=":
                return candidate_ver != constraint_ver
            case _:
                raise ValueError(f"unsupported operator: {self.operator}")


@dataclass
class Version:
    """Package dependency version and transitive deps."""

    number: str
    dependencies: list[Constraint]


@dataclass
class Package:
    """Singular package."""

    name: str
    versions: dict[str, Version]
