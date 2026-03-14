from lock_on.models import Constraint
from lock_on.resolver import Resolver


class DPLL(Resolver):
    def __init__(self):
        super().__init__()

    def resolve(self, verbose=False) -> None:
        """
        Recursive backtracker

        targets newest package order
        """
        self.verbose = verbose

        solution: dict[str, str] = {}

        _ = self._dpll(constraints=self.requirements, solution=solution)

        if solution:
            self._log("solution found! Writing to lock file", self.GREEN, override=True)
            self._write_to_lock_file(solution=solution)
        else:
            self._log(
                "no solution found for provided requirements.txt!",
                self.RED,
                override=True,
            )

    def _unit_propagate(self, constraints: list[Constraint], solution: dict):
        conflict = False
        forced = {}
        new_constraints = []

        # group constraints by package name
        grouped = {}
        for c in constraints:
            grouped.setdefault(c.package_name, []).append(c)

        while True:
            found_any = False

            for pkg_name, group in list(grouped.items()):
                if pkg_name in solution:
                    continue

                pkg = self.index[pkg_name]
                candidates = [
                    v for v in pkg.versions if all(c.is_satisfied_by(v) for c in group)
                ]

                match len(candidates):
                    case 0:
                        conflict = True
                        self._log(
                            f"unit propagation conflict: no valid version for {pkg_name}",
                            self.RED,
                        )
                        return conflict, forced, new_constraints
                    case 1:
                        self._log(
                            f"unit propagation forced {pkg_name}={candidates[0]}",
                            self.GREEN,
                        )
                        forced[pkg_name] = candidates[0]
                        solution[pkg_name] = candidates[0]
                        deps = self.index[pkg_name].versions[candidates[0]].dependencies
                        new_constraints += deps
                        for dep in deps:
                            grouped.setdefault(dep.package_name, []).append(dep)
                        found_any = True

            if not found_any:
                break

        return conflict, forced, new_constraints

    def _dpll(self, constraints: list[Constraint], solution: dict) -> bool:

        try:
            conflict, forced, new_constraints = self._unit_propagate(
                constraints=constraints, solution=solution
            )

            self._log(
                f"unit propagation resolved {len(forced)} package(s): {forced}",
                self.GREEN,
            )

            if conflict:
                return False

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
                    f"{pkg.name} in solution with version {solution[pkg.name]}",
                    self.YELLOW,
                )

                if constraint.is_satisfied_by(solution[pkg.name]):
                    self._log(
                        f"rechecking {pkg.name} with version {solution[pkg.name]}",
                        self.YELLOW,
                    )

                    return self._dpll(constraints[1:] + new_constraints, solution)

                self._log(
                    f"{pkg.name} with version {solution[pkg.name]} not satisfied!",
                    self.RED,
                )

                return False

            for pkg_ver in pkg.versions:
                self._log(f"trying {pkg.name} version {pkg_ver}", self.YELLOW)

                if constraint.is_satisfied_by(pkg_ver):
                    solution[pkg.name] = pkg_ver

                    # recursively call backtrack but without initial constraint
                    if self._dpll(
                        constraints=constraints[1:]
                        + pkg.versions[pkg_ver].dependencies
                        + new_constraints,
                        solution=solution,
                    ):
                        self._log(
                            f"{pkg.name} version {pkg_ver} satisfied!", self.GREEN
                        )

                        return True

                    self._log(f"{pkg.name} version {pkg_ver} not satisfied", self.RED)

                    solution.pop(pkg.name)
        finally:
            for key in forced:
                solution.pop(key)

        return False
