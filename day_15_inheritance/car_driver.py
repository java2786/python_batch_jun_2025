class Car:
    def startCar(self):
        print("Car is running")
    def applyBreak(sefl):
        print("Car is stopped")
        
class Driver:
    def __init__(self):
        self.car = Car()
        
    def drive(self):
        print("Driver is driving")
        self.car.startCar()
        self.car.applyBreak()    
    
driver = Driver()
driver.drive()
        