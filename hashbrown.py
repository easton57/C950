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
    def __init__(self) -> None:
        self.packages = HashIt()

    def set_package(self, id=None, deliv_addr=None, deliv_deadline=None, deliv_city=None, deliv_zip=None, deliv_weight=None, deliv_status=None, note=None, package=None) -> None:
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

    def package_search(self, search_term, search_field: str) -> None:
        """ Search function that returns all packages that contain the term in any field """
        matched_packages = []

        # Pull each package and check to see if any aspect conatains the search_term
        for i in range(1, self.packages.size + 1):
            package = self.packages.get(i)

            if str(search_term) in str(package.get(search_field)):
                matched_packages.append(package)

        if len(matched_packages) != 0:
            print("The following packages contain a match to your search term:")

            for i in matched_packages:
                print(i)
        else:
            print("Search results are empty! Please verify your search term and field.")

    def __str__(self) -> str:
        """ Print the packages in a nice way """
        return self.packages.__str__()
