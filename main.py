# Easton Seidel: 007806406
import math
import pandas as pd
from graphs import Graph
from truck import Truck
from hashbrown import HashIt, Packages


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

    # Account for any oddballs
    delayed = Packages()
    size = all_packages.size()

    for i in range(size):
        try:    # Clean this up, ew
            if all_packages.get_package(i).get("Special Note").__contains__("Delayed"):
                delayed.set_package(package=all_packages.get_package(i))
                all_packages.get_package(i).set("Delivery Status", "Delayed")
            elif all_packages.get_package(i).get("Special Note").__contains__("truck"):
                # Get the truck number
                num = int(all_packages.get_package(i).get("Special Note")[-1])

                trucks[num - 1].add_package(all_packages.get_package(i))
                all_packages.get_package(i).set("Delivery Status", f"On Truck {num} for Delivery")
        except Exception:
            print(f"Package with id {i} has no notes!")
            size += 1

    # create package lists based on theoretic max amount of packages
    theoretic_max = all_packages.size() // total_trucks

    # Calculate time and miles

    # Execute the routes
    pass


if __name__ == "__main__":
    main()
