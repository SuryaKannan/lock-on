from lock_on.base_manager import PackageManager


class BackTracker(PackageManager):
    def __init__(self):
        super().__init__()

    def resolve(self) -> None:
        pass
