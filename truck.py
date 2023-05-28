# Truck object file

class Truck:
    def __init__(self):
        self.packages = []
        self.drivers = 2
        self.speed = 18 # in mph

    def add_package(self, new_package, location, special_note=False):
        if len(self.packages) == 16:
            return False
        else:
            self.packages.append(new_package)
            return True

    def drop_package(self, package):
        self.packages.remove(package)
