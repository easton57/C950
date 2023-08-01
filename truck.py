# Truck object file

class Truck:
    def __init__(self):
        self.packages = []
        self.drivers = 2
        self.speed = 18  # in mph
        self.status = "Parked"
        self.route = []
        self.mileage = 0

    def add_package(self, new_package):
        if len(self.packages) == 16:
            return False
        else:
            self.packages.append(new_package)
            return True

    def drop_package(self, package):
        self.packages.remove(package)

    def change_status(self):
        if self.status == "Parked":
            self.status = "Out for Deliveries"
        else:
            self.status = "Parked"

    def update_mileage(self, miles):
        self.mileage += miles
