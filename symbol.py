
class Symbol:

    def __init__(self) -> None:
        pass

ALPHA = Symbol()
ALPHA_C = Symbol()
BETA = Symbol()
BETA_C = Symbol()

class PolicySymbol(Symbol):

    def __init__(self, number) -> None:
        super().__init__()
        self.number = number