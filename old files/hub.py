# Object file for the hub

class Hub:
    def __init__(self, packages):
        self.packages = packages    # Should be an dictionary, ID: Location

    def is_empty(self):
        if len(self.packages) == 0:
            return True
        else:
            return False
        
    def remaining_packages(self):
        return self.packages
    
    # optimize route

    # update address
    def update_location(self, id, location):
        try:
            self.packages[id] = location
            # re-optimize route
            return print("Successfully changed package location!")
        except Exception:
            return print("Error! Package may already be on a truck!")