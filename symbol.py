
class Symbol:

    def __init__(self) -> None:
        pass

class SymbolInfo:
    
    def __init__(self, policy_count) -> None:
        self.ALPHA = Symbol()
        self.ALPHA_C = Symbol()
        self.BETA = Symbol()
        self.BETA_C = Symbol()
        self.POLICY = [Symbol() for _ in range(policy_count)]