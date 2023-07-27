# Easton Seidel: 007806406
import math
import pandas as pd
from graphs import Graph
from truck import Truck
from hashbrown import HashIt, Packages


def locate_df_index(df, key):
    for i in range(len(df.index)):
        if key in df.iloc[i][1][0] or key in df.iloc[i][0]:
            return i
        elif key in df.iloc[i][1] or key in df.iloc[i][0]:
            return i


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
    distances_df = pd.DataFrame(distances).iloc[7:]  # This is starting on column one
    packages_df = pd.DataFrame(packages).iloc[7:]

    distances_headers = pd.DataFrame(distances).iloc[6]
    packages_headers = pd.DataFrame(packages).iloc[6]

    # Cleanup addresses at the beginning of the rows
    for i in range(len(distances_df.index)):
        distances_df.iloc[i][0] = distances_df.iloc[i][0].replace('\n', ' ')
        distances_df.iloc[i][0] = distances_df.iloc[i][0].replace('  ', ' ')
        distances_df.iloc[i][1] = distances_df.iloc[i][1].replace('\n', ' ')
        distances_df.iloc[i][1] = distances_df.iloc[i][1].replace('  ', ' ')

    # Cleanup distances dataframe headers
    for j in range(29):
        if type(distances_headers.iloc[j]) is not float:
            distances_headers.iloc[j] = distances_headers.iloc[j].replace('\n', ' ')
            distances_headers.iloc[j] = distances_headers.iloc[j].replace('  ', ' ')

    # Assign Dataframe headers
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

        stop_map.add_vertex([row[0], row[1]])

    # add the edges
    for i in range(len(distances_df.index)):
        row = distances_df.iloc[i]

        for j in range(2, 29):
            if not math.isnan(row[j]):
                stop_map.add_edge(row[0], distances_headers.iloc[j].replace('\n', ' '), row[j])

    # filter some stuff
    size = all_packages.size()

    delayed = []
    paired = []
    time_critical = []
    truck_specific = []
    wrong_address = []

    for i in range(total_trucks):
        truck_specific.append([])

    for i in range(1, size + 1):
        curr_pack = all_packages.get_package(i)

        if type(curr_pack.get("Delivery Deadline")) is not str:  # Delivered by a specific time?
            time_critical.append(curr_pack)

        try:
            if "Delayed" in curr_pack.get("Special Note"):  # Delayed oh gosh
                delayed.append(all_packages.get_package(i).get("Package ID"))

            elif "truck" in curr_pack.get("Special Note"):  # Need a specific truck?
                # Get the truck number and add to the truck_specific slot
                num = int(curr_pack.get("Special Note")[-1])
                truck_specific[num - 1].append(all_packages.get_package(i).get("Package ID"))

            elif "Must be delivered with" in curr_pack.get("Special Note"):  # What packages need to be paired?
                deliv_list = curr_pack.get("Special Note").replace(",", "").split(" ")[4:]
                deliv_list = [int(id) for id in deliv_list]

                package_id = all_packages.get_package(i).get("Package ID")

                paired.append([package_id] + deliv_list)

            elif "Wrong address" in curr_pack.get("Special Note"):
                wrong_address.append(all_packages.get_package(i).get("Package ID"))

        except Exception as e:
            print(f"Package with id {i} has no notes!")
            size += 1

    # some var cleanup for my sake
    del curr_pack, distances_headers, packages_headers, distances, packages, size, row, i, j, num, package_id, deliv_list

    # Merge paired packages list's where things are common
    for i in paired:
        for j in i:
            list_size = len(paired)

            for k in paired:
                if j in k and i != k:
                    paired.append(list(set(i).union(set(k))))
                    paired.remove(i)
                    paired.remove(k)
                    break

            if list_size > len(paired):
                break

    # Add each package to it's spot on the graph
    for i in range(1, all_packages.size() + 1):
        pack_id = all_packages.get_package(i).get('Package ID')
        address = all_packages.get_package(i).get('Delivery Address')
        new_label = stop_map.get_full_label(address)

        new_label.append(str(pack_id))

        stop_map.update_vertex(address, new_label)

    # Remove stops that don't have packages? (In this case there aren't any, but it would be useful for future proofing)

    # Create the routes
    max_miles = 140  # Per project requirements (for all trucks combined)
    mpm = trucks[0].speed / 60
    start_time = "8:00:00 am"

    # Generate every possible route? No sir
    possible_routes = HashIt()
    undelivered = list(range(1, all_packages.size() + 1))
    used_stops = []

    for i in stop_map.labels:
        packages = []
        new_route = []
        length = 0

        if "HUB" not in i[1]:
            new_route.append(stop_map.labels[0])
            new_route.append(i)

            # Set inital length from hub to first stop
            length += stop_map.get_weight(stop_map.labels[0][1], i[1])

            if length == 0 or length == math.inf:
                length = 0
                length += stop_map.get_weight(i[1], stop_map.labels[0][1])

            # Save the packages
            packages += i[2:]

            # Build the route until 16 package limit is reached
            while len(packages) < 16:
                next_stop = None
                next_dist = math.inf

                # find the next closest spot
                for j in stop_map.labels:
                    test_dist = stop_map.get_weight(new_route[-1][1], j[1])

                    if test_dist < next_dist and j not in new_route:
                        next_stop = j
                        next_dist = test_dist

                    test_dist = stop_map.get_weight(j[1], new_route[-1][1])

                    if test_dist < next_dist and j not in new_route:
                        next_stop = j
                        next_dist = test_dist

                # Make sure we aren't packing to many packages
                tmp = packages + next_stop[2:]

                if len(tmp) > 16:
                    break

                # Save the new values
                packages += next_stop[2:]
                length += next_dist
                new_route.append(next_stop)

            # Add the hub as the last stop
            new_route.append(stop_map.labels[0])

            # Save the route as the first stop as the key with the whole route, packages and length as a value
            possible_routes.set(new_route[1][1], [new_route, length, packages])

    # find a route that matches paired out of the ideal efficient routes
    paired_routes = []

    for i in paired:
        for j in stop_map.labels:
            if "HUB" not in j[1] and i in possible_routes.get(j[1])[2]:
                paired_routes.append(possible_routes.get(j[1]))

    # if paired routes is empty, create one

    # Find a route that matches truck requirements
    truck_specific_routes = []

    for i in truck_specific:
        if len(i) != 0:
            for j in stop_map.labels:
                if "HUB" not in j[1] and i in possible_routes.get(j[1])[2]:
                    truck_specific_routes.append(possible_routes.get(j[1]))

    # If truck specific routes is empty, create one

    # Find a route that matches delayed flights

    pass


if __name__ == "__main__":
    main()