class Car:
   def __init__(self, id, client):
        self.id = id
        self.client = client

   def get_cost_hour(self):
      return 10