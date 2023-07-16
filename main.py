# Easton Seidel: 007806406
import math
import pandas as pd
from graphs import Graph
from truck import Truck
from hashbrown import HashIt, Packages

'''
Depending on how the current mess goes, here's an idea to make it better.
Instead of go package by package, go based requirement by requirement to mitigate any possible mix-ups if paired 
packages also have a truck requirement

Create arrays of paired packages
    [All those that are paired including possible packages that have a truck requirement]
        Then place them on the required truck if any have a truck requirement
            [array of 4 packages, oh 3 has a truck requirement? Place all on that truck]
'''


def main():
    # Define our trucks
    total_trucks = 3
    trucks = []

    for i in range(total_trucks):
        trucks.append(Truck())

    # Simulation variable, False, follows true time of day, True, 1 minute = 1 second
    sim_routes = True

    # Define our packages hashmap
    all_packages = Packages()

    # import our xlsx files
    distances = pd.read_excel("./project_files/WGUPS Distance Table.xlsx")
    packages = pd.read_excel("./project_files/WGUPS Package File.xlsx")

    # Get what we care about
    distances_df = pd.DataFrame(distances).iloc[7:]
    packages_df = pd.DataFrame(packages).iloc[7:]

    distances_headers = pd.DataFrame(distances).iloc[6]
    packages_headers = pd.DataFrame(packages).iloc[6]

    distances_df = distances_df.set_axis(distances_headers, axis=1)
    packages_df = packages_df.set_axis(packages_headers, axis=1)

    # Plug packages into our hashmap
    for i in range(len(packages_df.index)):
        row = packages_df.iloc[i]

        all_packages.set_package(row[0], row[1], row[5], row[2], row[4], row[6], "Undelivered", row[7])

    # Make a graph with our locations
    stop_map = Graph(len(distances_df.index))

    # add the vertices
    for i in range(len(distances_df.index)):
        row = distances_df.iloc[i]

        stop_map.add_vertex(row[0].replace('\n', ' '))

    # add the edges
    for i in range(len(distances_df.index)):
        row = distances_df.iloc[i]

        for j in range(2, 29):
            if not math.isnan(row[j]):
                stop_map.add_edge(row[0].replace('\n', ' '), distances_headers.iloc[j].replace('\n', ' '), row[j])

    # Generate all possible routes
    routes = []

    for i in stop_map.labels:
        for j in stop_map.labels:
            path = stop_map.dijkstra_shortest_path(i, j)
            if path[0] != math.inf:
                routes.append(path)

    # Sort them by route length
    routes.sort()
    i = 0

    # remove any that are distance of 0 or stop len of < 2
    while i != len(routes):
        if routes[i][0] == 0.0 or len(routes[i][1]) <= 2:
            routes.remove(routes[i])
        else:
            i += 1

    # Account for any oddballs
    size = all_packages.size()

    for i in range(size):
        try:    # Clean this up, ew
            curr_pack = all_packages.get_package(i).get("Special Note")

            if curr_pack.__contains__("Delayed"):
                all_packages.get_package(i).set("Delivery Status", "Delayed")
            elif curr_pack.__contains__("truck"):
                # Get the truck number
                num = int(all_packages.get_package(i).get("Special Note")[-1])

                trucks[num - 1].add_package(all_packages.get_package(i))
                all_packages.get_package(i).set("Delivery Status", f"On Truck {num} for Delivery")
            elif curr_pack.__contains__("Must be delivered with"):
                deliv_list = curr_pack.replace(",", "").split(" ")[4:]
                deliv_list = [int(id) for id in deliv_list]
                placed = False
                truck = 0
                least = 99999999

                while not placed:
                    if truck == len(trucks) and not placed:
                        truck = least
                        break

                    if least == 99999999 or len(trucks[truck].packages) < len(trucks[least].packages):
                        least = truck

                    # Check to see if dependents are on the truck already
                    for j in trucks[truck].packages:
                        if j.get("Package ID") in deliv_list:
                            placed = True

                    if not placed:
                        truck += 1

                # Change the status and add all extra packages to that truck
                # Change the status note and add to the truck
                all_packages.get_package(i).set("Delivery Status", f"On truck {truck} for Delivery")
                trucks[truck].add_package(all_packages.get_package(i))

                # Add extra packages
                for j in deliv_list:
                    if all_packages.get_package(j) not in trucks[truck].packages:
                        trucks[truck].add_package(all_packages.get_package(j))
                        all_packages.get_package(j).set("Delivery Status", f"On truck {truck} for Delivery")

        except Exception as e:
            print(f"Package with id {i} has no notes! {e}")
            size += 1

    # create package lists based on theoretic max amount of packages
    max_pack = 16  # Per project requirements

    # Calculate time and miles
    mph = 18  # Per project requirements
    max_miles = 140  # Per project requirements (for all trucks combined)

    # Execute the routes
    pass


if __name__ == "__main__":
    main()
