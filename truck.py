# Truck object file

class Truck:
    def __init__(self):
        self.packages = []
        self.drivers = 2

    def add_package(self, new_package, location, special_note=False):
        if len(self.packages) == 16:
            return False
        else:
            self.packages.append(new_package)
            return True