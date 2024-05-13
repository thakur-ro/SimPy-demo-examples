import simpy 
from random import choice

from entities.pallets import Pallet
from entities.staging_area import StagingArea
from entities.trailers import Trailer
from entities.doors import Door
from resources.dock_worker import DockWorker

class DistributionCenter:
    def __init__(self, env: simpy.Environment, pallet_interval: int, trailer_interval: int, staging_capacity: int, doors: int, workers: int,trailer_capacity:int):
        self.env = env
        self.pallet_interval = pallet_interval
        self.trailer_interval = trailer_interval
        self.staging_capacity = staging_capacity
        self.trailer_capacity = trailer_capacity
        self.doors = doors
        self.workers = workers

        self.skipped_trailers = 0
        self.dropped_pallets = 0
        self.generated_trailers = 0
        self.generated_pallets = 0

        self.staging_area = StagingArea(env, staging_capacity)
        self.doors = [Door(env) for i in range(doors)]
        self.dock_workers = [DockWorker(env) for i in range(workers)]

    def p_choose_door(self) -> Door:
        available_doors = [d for d in self.doors if d.is_available]
        return choice(available_doors) if available_doors else None
    
    def p_assign_worker(self,assigned_door:Door)->None:
        for worker in self.dock_workers:
            yield self.env.process(worker.work(self.staging_area,assigned_door))
            break

    def p_pallet_generator(self) -> None:
        while True:
            yield self.env.timeout(self.pallet_interval)
            pallet = Pallet(self.env,self.generated_pallets)
            print(f"Env {self.env.now}: Pallet {self.generated_pallets} generated")
            if len(self.staging_area.store.items) < self.staging_area.capacity:
                yield self.staging_area.store.put(pallet)
                print(f"Env {self.env.now}: Pallet {self.generated_pallets} stored in staging")
            else:
                self.dropped_pallets+=1
                print(f"Env {self.env.now}: Pallet {self.generated_pallets} dropped due to full staging area")
            self.generated_pallets += 1

    def p_trailer_generator(self) -> None:
        while True:
            yield self.env.timeout(self.trailer_interval)
            trailer = Trailer(self.env,capacity=self.trailer_capacity) 
            # Find available doors
            assigned_door = self.p_choose_door()
            if assigned_door is None:
                self.skipped_trailers+=1
                print(f"Env {self.env.now}: Trailer {self.generated_trailers} skipped due to no available doors")                
            else:
                with assigned_door.door_resource.request() as request:
                    yield request
                    print(f"Env {self.env.now}: Trailer assigned to door")
                    assigned_door.trailer = trailer
                    assigned_door.is_available = False
                    yield self.env.process(self.p_assign_worker(assigned_door))
                    print(f"Env {self.env.now}: Trailer released from door")
                assigned_door.trailer = None
                assigned_door.is_available = True

            self.generated_trailers += 1

def main():
    pallet_interval = 30  
    trailer_interval = 5
    staging_capacity = 100
    doors = 5 
    workers = 3  
    trailer_capacity = 30

    env = simpy.Environment()
    dc = DistributionCenter(env, pallet_interval, trailer_interval, staging_capacity, doors, workers,trailer_capacity)
    env.process(dc.p_pallet_generator())
    env.process(dc.p_trailer_generator())
    env.run(until=1000)
    print(f"Total skipped trailers {dc.skipped_trailers}")
    print(f"Total dropped pallets {dc.dropped_pallets}")
    print(f"Total completed trailer loads {dc.generated_trailers}")
    print(f"Total generated pallets {dc.generated_pallets}")
    print(env.now)



if __name__ == "__main__":
    main()
