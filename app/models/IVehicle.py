class IVehicle(object):
    def __init__(self, id, client):        
        self.id = id
        self.client = client
        self.get_cost_hour()