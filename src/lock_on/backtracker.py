from typing import TYPE_CHECKING

from lock_on.base_manager import PackageManager

if TYPE_CHECKING:
    from lock_on.models import Constraint


class BackTracker(PackageManager):
    def __init__(self):
        super().__init__()

    def resolve(self) -> None:
        """
        Recursive backtracker

        targets newest package order
        """
        solution: dict[str, str] = {}

        _ = self._backtrack(constraints=self.requirements, solution=solution)

        if bool(solution):
            self._write_to_lock_file(solution=solution)
        else:
            print("No solution found!")

    def _backtrack(self, constraints: list[Constraint], solution: dict) -> bool:
        if not constraints:
            return True

        # only handle first constraint
        constraint = constraints[0]

        msg = f"solving {constraint.package_name} for version {constraint.version}"
        self._log(msg, self.YELLOW)

        pkg = self.index[constraint.package_name]

        # check if package is already in solution, disregard initial constraint
        if pkg.name in solution:
            msg = f"{pkg.name} in solution with version {solution[pkg.name]}"
            self._log(msg, self.YELLOW)

            if constraint.is_satisfied_by(solution[pkg.name]):
                msg = f"rechecking {pkg.name} with version {solution[pkg.name]}"
                self._log(msg, self.YELLOW)

                return self._backtrack(constraints[1:], solution)

            msg = f"{pkg.name} with version {solution[pkg.name]} not satisfied!"
            self._log(msg, self.RED)

            return False

        for pkg_ver in pkg.versions:
            msg = f"trying {pkg.name} version {pkg_ver}"
            self._log(msg, self.YELLOW)

            if constraint.is_satisfied_by(pkg_ver):
                solution[pkg.name] = pkg_ver

                # recursively call backtrack but without initial constraint
                if self._backtrack(
                    constraints=constraints[1:] + pkg.versions[pkg_ver].dependencies,
                    solution=solution,
                ):
                    msg = f"{pkg.name} version {pkg_ver} satisfied!"
                    self._log(msg, self.GREEN)

                    return True

                msg = f"{pkg.name} version {pkg_ver} not satisfied"
                self._log(msg, self.RED)

                solution.pop(pkg.name)

        return False
