from datetime import time
from datetime import datetime
from . import Car
from . import Client
class Local:
    def __init__(self, id, vehicle, arrival_time):
        self.id = id
        self.vehicle = vehicle
        self.arrival_time = arrival_time
    
    def is_empty(self):
        return self.vehicle == None

    def duration_time_parked(self):
        if(self.is_empty()):
            raise ValueError()
        return (datetime.now() - self.arrival_time).total_seconds()

    def get_cost(self):
        hours = self.duration_time_parked() / 3600
        return self.vehicle.get_cost_hour() * hours

