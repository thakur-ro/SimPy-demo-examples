import simpy


class StagingArea:
    def __init__(self, env: simpy.Environment, capacity: int) -> None:
        self.env: simpy.Environment = env
        self.capacity: int = capacity
        self.store: simpy.Store = simpy.Store(env, capacity)
