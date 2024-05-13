import simpy

from entities.staging_area import StagingArea
from entities.doors import Door

class DockWorker:
    def __init__(self, env: simpy.Environment) -> None:
        self.env: simpy.Environment = env
        self.worker_resource: simpy.Resource[object] = simpy.Resource(env, capacity=1) 

    def work(self, staging_area: StagingArea, door: Door) -> None:
        with self.worker_resource.request() as req: 
            print(f"Env {self.env.now}: Dock worker assigned")
            yield req  
            trailer = door.trailer
            while trailer and trailer.pallets < trailer.capacity:
                if len(staging_area.store.items) > 0:
                    pallet = yield staging_area.store.get()
                    print(f"Env {self.env.now}: Dock worker loaded the pallet")
                    yield self.env.process(trailer.load(pallet))

                else:
                    print(f"Env {self.env.now}: waiting for pallet")                    
                    yield self.env.timeout(5)  # Wait for pallets if none available

            print(f"Env {self.env.now}: Dock worker released and trailer load complete")
