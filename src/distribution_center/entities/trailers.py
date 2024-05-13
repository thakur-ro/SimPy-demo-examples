import simpy


class Trailer:
    def __init__(self, env: simpy.Environment, capacity: int = 30) -> None:
        self.env: simpy.Environment = env
        self.capacity: int = capacity
        self.pallets: int = 0
#trailer could be store
    def load(self,pallet) -> None:
            self.pallets += 1
            yield self.env.timeout(10)