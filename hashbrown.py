# My hash file for the hash algos for the distances and packages

class HashIt:
    # Initialize the hashtable with default size of 1
    def __init__(self) -> None:
        self.size = 1
        self.hash_table = [[] for _ in range(self.size)]

    # Resize the array by adding one point
    def resize(self) -> None:
        self.size += 1

        self.hash_table.append([])

    def is_empty(self) -> bool:
        for i in range(self.size):
            if self.hash_table[i]:
                return False
            
        return True
        
    # Set a value in the hashtable
    def set(self, key, value) -> None:
        written = False

        # See if the table is empty and add size if needed
        if not self.is_empty() and self.get(key) is False:
            self.resize()

        # get a hash value
        hash_key = hash(key) % self.size

        # make sure our has value is pointing to an empty spot, otherwise find the next empty spot
        while not written:
            if self.hash_table[hash_key] == [] or self.hash_table[hash_key][0] == key:
                # Place the value in the thing
                self.hash_table[hash_key] = [key, value]
                written = True
            else:
                hash_key += 1

                if hash_key >= self.size:
                    hash_key = 0

    # Get function
    def get(self, key) -> str or bool:
        read = False

        # get a hash value
        hash_key = hash(key) % self.size

        # Find the value for the key
        while not read:
            if self.hash_table[hash_key][0] == key:
                return self.hash_table[hash_key][1]
            else:
                hash_key += 1

                if hash_key >= self.size:
                    hash_key = 0

            if hash_key == hash(key) % self.size:
                return False

    # drop function
    def drop(self, key) -> bool:
        dropped = False

        # get a hash value
        hash_key = hash(key) % self.size

        # Find the value for the key
        while not dropped:
            if self.hash_table[hash_key][0] == key:
                self.hash_table.pop(hash_key)
                return True
            else:
                hash_key += 1

                if hash_key >= self.size:
                    hash_key = 0

            if hash_key == hash(key) % self.size:
                return False

    # Print the table in a nice way
    def __str__(self) -> str:
        final_str = ""

        for i in self.hash_table:
            final_str += f"{i[0]}: {i[1]}\n"

        return final_str


class Packages:
    packages = HashIt()

    def set_package(self, id, deliv_addr, deliv_deadline, deliv_city, deliv_zip, deliv_weight, deliv_status, note, package=None) -> None:
        if id is not None:
            package = HashIt()
            package.set("Package ID", id)
            package.set("Delivery Address", deliv_addr)
            package.set("Delivery Deadline", deliv_deadline)
            package.set("Delivery City", deliv_city)
            package.set("Delivery Zip Code", deliv_zip)
            package.set("Delivery Weight", deliv_weight)
            package.set("Delivery Status", deliv_status)
            package.set("Special Note", note)

            self.packages.set(id, package)
        else:
            self.packages.set(package.get("Package ID"), package)

    def get_package(self, id) -> HashIt:
        return self.packages.get(id)
    
    def size(self) -> int:
        return self.packages.size

    # Print the table in a nice way
    def __str__(self) -> str:
        return self.packages.__str__()