from datatime import datatime

at = 120

if __name__ == "__main__":
    client = Client(0, "Carlos", "teste@gmail.com", "00-0000.0000")
    car = Car(0, client)
    localmanager = LocalManager(10)

    localmanager.insert_vehicle(car)
    time.sleep(at)
    
    print(arrival_time)

