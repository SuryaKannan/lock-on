from dataclasses import dataclass
import re

@dataclass
class Constraint:
    """Singular package specifc constraint."""
    target_package_name: str
    operator: str
    version: str

    @classmethod
    def from_string(cls, constraint: str) -> Constraint:

        match = re.match(
            pattern=r"([a-z-]+)([><=!]+)([\d.]+)", 
            string=constraint
        )

        if match is not None:
            name, op, ver = match.groups()
            return cls(target_package_name=name, operator=op, version=ver)
        else:
            raise ValueError("invalid contraint in graph")
    

    def is_satisfied_by(self, candidate: str) -> bool:
        return False

@dataclass
class Version:
    """Singular package."""
    number: str
    dependencies: list[Constraint]

@dataclass
class Package:
    """Singular package."""
    name: str
    versions: dict[str, Version]
