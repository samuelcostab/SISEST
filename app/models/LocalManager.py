from . import Local
from . import Car
from datetime import datetime
class LocalManager:
    def __init__(self, size):
        self.size = size
        self.locals = []
        for index in range(size):
            self.locals.append(Local(index, None, None))
    
    def insert_vehicle(self, vehicle):
        for local in self.locals:
            if not local.is_empty():
                continue            
            local.vehicle = vehicle
            local.arrival_time = datetime.now()
            break
    def remove_vehicle(self, vehicle_id):
        for local in self.locals:
            if not local.is_empty() and local.vehicle.id == vehicle_id:
                value = local.get_cost()
                local.arrival_time = None
                local.vehicle = None
                return value
    def free_locals(self):
        count = 0
        for local in self.locals:
            if local.is_empty():
                count += 1
        return count