# Truck object file

class Truck:
    def __init__(self, truck_number):
        self.number = truck_number
        self.packages = []  # Dictionary for ID: location, max 16
        self.drivers = 2

    def add_package(self, new_package, location, special_note=False):
        if len(self.packages) > 16:
            return False
        else:
            self.packages[new_package] = location
            self.special_note[new_package] = special_note
            return True