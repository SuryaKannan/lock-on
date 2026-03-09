from lock_on.resolver import Resolver


class PubGrub(Resolver):
    def __init__(self):
        super().__init__()

    def resolve(self, verbose=False) -> None:
        self.verbose = verbose
        pass
