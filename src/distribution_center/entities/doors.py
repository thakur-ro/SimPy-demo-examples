import simpy


class Door:
    def __init__(self, env: simpy.Environment) -> None:
        self.env: simpy.Environment = env
        self.door_resource: simpy.Resource[object] = simpy.Resource(env, capacity=1)  
        self.trailer = None
        self.is_available = True
    
