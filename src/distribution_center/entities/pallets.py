import simpy 

class Pallet:
    def __init__(self, env: simpy.Environment,id: int) -> None:
        self.env: simpy.Environment = env
        self.id: int = id
