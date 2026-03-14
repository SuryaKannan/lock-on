from lock_on.models import Constraint
from lock_on.resolver import Resolver


class BackTracker(Resolver):
    def __init__(self):
        super().__init__()

    def resolve(self, verbose=False) -> None:
        """
        Recursive backtracker

        targets newest package order
        """
        self.verbose = verbose

        solution: dict[str, str] = {}

        _ = self._backtrack(constraints=self.requirements, solution=solution)

        if solution:
            self._log("solution found! Writing to lock file", self.GREEN, override=True)
            self._write_to_lock_file(solution=solution)
        else:
            self._log(
                "no solution found for provided requirements.txt!",
                self.RED,
                override=True,
            )

    def _backtrack(self, constraints: list[Constraint], solution: dict) -> bool:
        if not constraints:
            return True

        # only handle first constraint
        constraint = constraints[0]

        self._log(
            f"solving {constraint.package_name} for version {constraint.version}",
            self.YELLOW,
        )

        pkg = self.index[constraint.package_name]

        # check if package is already in solution, disregard initial constraint
        if pkg.name in solution:
            self._log(
                f"{pkg.name} in solution with version {solution[pkg.name]}", self.YELLOW
            )

            if constraint.is_satisfied_by(solution[pkg.name]):
                self._log(
                    f"rechecking {pkg.name} with version {solution[pkg.name]}",
                    self.YELLOW,
                )

                return self._backtrack(constraints[1:], solution)

            self._log(
                f"{pkg.name} with version {solution[pkg.name]} not satisfied!", self.RED
            )

            return False

        for pkg_ver in pkg.versions:
            self._log(f"trying {pkg.name} version {pkg_ver}", self.YELLOW)

            if constraint.is_satisfied_by(pkg_ver):
                solution[pkg.name] = pkg_ver

                # recursively call backtrack but without initial constraint
                if self._backtrack(
                    constraints=constraints[1:] + pkg.versions[pkg_ver].dependencies,
                    solution=solution,
                ):
                    self._log(f"{pkg.name} version {pkg_ver} satisfied!", self.GREEN)

                    return True

                self._log(f"{pkg.name} version {pkg_ver} not satisfied", self.RED)

                solution.pop(pkg.name)

        return False
