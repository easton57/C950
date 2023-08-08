# Easton Seidel: 007806406
import sys
import datetime
import math
import copy
import time
import threading
import tkinter as tk
import pandas as pd
import datetime as dt
from graphs import Graph
from truck import Truck
from tkinter import ttk, messagebox
from threading import Thread
from hashbrown import HashIt, Packages


interval = 0
curr_time = [7, 45]
sim = False
shutdown = False
complete = False
over_miles = False
traveled_miles = 0
delayed = []
paired = []
time_critical = []
wrong_address = []
all_packages = Packages()


def update_table():
    """ Dynamically reset the table time and package status's """
    global shutdown, complete, over_miles, traveled_miles

    # Show a pop-up when the routes have finished being created and assigned
    if complete:
        messagebox.showinfo("Route Completed",
                            "Routes are completed. Please allow them to finish executing after closing this pop-up.")
        complete = False

    if over_miles:
        messagebox.showerror("Over Miles!",
                             "Created routes exceed the mile limit for your trucks. "
                             "Please check the routes and try again.")
        over_miles = False

    if not shutdown:
        # Update the time label with the current time or simulated time
        if sim:
            current_time = get_sim_time()
            time_label.config(text=f"Current Time: {current_time.isoformat(timespec='minutes')}\t"
                                   f"Miles Traveled: {format(traveled_miles, '5.2f')}")
        else:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            time_label.config(text="Current Time: " + current_time +
                                   f"\tMiles Traveled: {format(traveled_miles, '5.2f')}")

        # Clear existing rows in the table
        table.delete(*table.get_children())

        # Insert data into the table
        for i in range(1, all_packages.size() + 1):
            package = [all_packages.get_package(i).get("Package ID"),
                       all_packages.get_package(i).get("Delivery Deadline"),
                       all_packages.get_package(i).get("Delivery Status"),
                       all_packages.get_package(i).get("Special Note")]
            table.insert("", "end", values=package)

        # Schedule the update_table function to run again after 1 second
        root.after(1000, update_table)
    else:
        print("Shutting down application...")


def on_close():
    """ Close function for when the button is pressed """
    global shutdown
    shutdown = True
    root.destroy()
    sys.exit()


def create_package_table():
    """ Function for our status window """
    global root, table, time_label
    root = tk.Tk()
    root.title("Package Status")

    # Set dynamic adjustments
    root.pack_propagate(True)

    # Set close button to stop the program
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Set the initial window height to 500 pixels
    window_height = 500

    # Set the initial window size
    root.geometry(f"{775}x{window_height}")

    time_label = tk.Label(root, text="", font=("Helvetica", 12))
    time_label.pack()

    table = ttk.Treeview(root,
                         columns=("Package ID", "Delivery Deadline", "Delivery Status", "Special Note"),
                         show="headings", height=400)

    # Define column headings
    table.heading("Package ID", text="Package ID")
    table.heading("Delivery Deadline", text="Delivery Deadline")
    table.heading("Delivery Status", text="Delivery Status")
    table.heading("Special Note", text="Special Note")

    # Define column widths
    table.column("Package ID", width=75)
    table.column("Delivery Deadline", width=100)
    table.column("Delivery Status", width=250)
    table.column("Special Note", width=350)

    table.pack(fill="both", expand=True)
    update_table()
    root.mainloop()


def sim_time(new_interval: int) -> None:
    """ Cute little sim time function """
    global interval, shutdown, complete
    interval = new_interval

    while not shutdown or not complete:
        time.sleep(interval)
        curr_time[1] += 1

        if curr_time[1] == 60:
            curr_time[1] = 0
            curr_time[0] += 1

        if curr_time[0] == 24:
            break


def get_sim_time() -> time:
    """ Return the simulation time as a time """
    return dt.time(curr_time[0], curr_time[1])


def distance_calc(route: list, graph: Graph) -> float:
    """ Calculate the distance traveled of the given route """
    previous = None
    distance = 0

    for i in route:
        if not previous:
            previous = i
        else:
            distance_tmp = graph.get_weight(i[1], previous[1])

            distance += distance_tmp

    return distance


def shortest_route(routes: list, graph: Graph) -> list:
    """ Find the possibly shortest route with the given packages """
    # Check to see if there's one route or multiple
    if len(routes) != 1:
        shortest = None

        for i in routes:
            if not shortest:
                shortest = i
            elif distance_calc(shortest, graph) > distance_calc(i, graph):
                shortest = i

        return shortest
    else:
        return routes[0]


def get_route_packages(route) -> list:
    """ Get packages from the stops in the graph """
    packages = []

    for i in route:
        packages += i[2:]

    return packages


def create_route(packages: list, graph: Graph, first_stop: str = None) -> list:
    """ Create a route based on packages that are passed in """
    global delayed, paired, time_critical, wrong_address
    route = [graph.labels[0]]
    labels = []
    time_critical_labels = []
    wrong_address_labels = []

    if first_stop is not None:
        route = [first_stop]

    # Get the labels for the delayed package
    for i in graph.labels:
        for j in packages:
            if j in i and i not in labels \
                    and j not in time_critical and i not in time_critical_labels \
                    and j not in wrong_address and i not in wrong_address_labels:
                labels.append(i)
            elif j in i and i not in time_critical_labels \
                    and j not in wrong_address and i not in wrong_address_labels:
                if i in labels:
                    labels.remove(i)

                time_critical_labels.append(i)
            elif j in i and i not in wrong_address_labels and j in wrong_address:
                if i in labels:
                    labels.remove(i)
                elif i in time_critical_labels:
                    time_critical_labels.remove(i)

                wrong_address_labels.append(i)

    # add the time critical stops to the front of the route
    while len(time_critical_labels) > 0:
        closest = None

        for i in time_critical_labels:
            if closest is None and i not in route:
                closest = i
            elif i not in route and (
                    graph.get_weight(route[-1][1], i[1]) < graph.get_weight(route[-1][1], closest[1])
                    or graph.get_weight(i[1], route[-1][1]) < graph.get_weight(closest[1], route[-1][1])):
                closest = i

        route.append(closest)
        time_critical_labels.remove(closest)

    # Find the closest
    while len(labels) > 0:
        closest = None

        for i in labels:
            if closest is None and i not in route:
                closest = i
            elif i not in route and (graph.get_weight(route[-1][1], i[1]) < graph.get_weight(route[-1][1], closest[1])
                                     or graph.get_weight(i[1], route[-1][1]) < graph.get_weight(closest[1], route[-1][1])):
                closest = i

        route.append(closest)
        labels.remove(closest)

    # Find the closest for wrong address
    while len(wrong_address_labels) > 0:
        closest = None

        for i in wrong_address_labels:
            if closest is None and i not in route:
                closest = i
            elif i not in route and (
                    graph.get_weight(route[-1][1], i[1]) < graph.get_weight(route[-1][1], closest[1])
                    or graph.get_weight(i[1], route[-1][1]) < graph.get_weight(closest[1], route[-1][1])):
                closest = i

        route.append(closest)
        wrong_address_labels.remove(closest)

    # Always end the route at home
    route.append(graph.labels[0])

    return route


def insert_package(package: int, routes: list, graph: Graph) -> list:
    """ Insert package in the most efficient spot in the given route """
    most_efficient_route = None
    added_routes = []

    for i in routes:
        added_routes.append([create_route(i[2] + package, graph), distance_calc(create_route(i[2] + package, graph), graph), i[2] + package])

    for i in added_routes:
        if not added_routes or (i[1] < most_efficient_route[1] and len(i[2]) <= 16):
            most_efficient_route = i

    return most_efficient_route


def correct_address(package: HashIt, graph: Graph):
    global wrong_address, all_packages

    # Remove the package from the wrong address array
    package_id = package.get("Package ID")
    wrong_address.remove(package_id)
    package.set("Special Note", "Address Corrected")

    # Change the affected address in all_packages
    unfiltered_address = '410 S State St., Salt Lake City, UT 84111'
    new_city = unfiltered_address.split(',')[1]
    new_zip = unfiltered_address.split(',')[2].split(' ')[-1]
    new_address = " " + unfiltered_address.split(',')[0].replace('.', '') + f" ({new_zip})"
    package.set("Delivery Address", new_address)
    package.set("Delivery City", new_city)
    package.set("Delivery Zip Code", new_zip)

    # Remove the package from it's point on the graph and Add it to it's proper point
    for i in graph.labels:
        if package_id in i:
            i.remove(package_id)

        if new_address in i:
            i.append(package_id)


def execute_route(truck: Truck, graph: Graph) -> None:
    """ Function to execute the route """
    global shutdown, traveled_miles, wrong_address
    previous_stop = truck.route[0][0]
    distance_traveled = 0
    stop_distance = 0
    speed_per_min = (truck.speed / 60) / interval

    wrong_address_packages = []

    for i in wrong_address:
        wrong_address_packages.append(all_packages.get_package(i))

    # loop until it's go time
    while get_sim_time() <= truck.departure_time:
        # check for shutdown call
        if shutdown:
            exit()

        time.sleep(interval / 4)

    # Change status of those that are delayed
    for i in truck.packages:
        if "waiting for arrival" in i.get("Delivery Status"):
            i.set("Delivery Status", f"Package is on truck {truck.truck_id} for delivery")

    # Our execution loop to mark packages as delivered and track the distance traveled
    for i in range(1, len(truck.route[0])):
        # check for shutdown call
        if shutdown:
            exit()

        # Check for a wrong address package and recurse if there is one.
        if len(list(set(truck.packages).intersection(wrong_address_packages))) > 0 and curr_time >= [10, 20]:
            wrong_address_filtered = set(truck.packages).intersection(set(wrong_address_packages))

            # remove them from wrong_address so they'll be placed earlier in the route
            for j in wrong_address_filtered:
                correct_address(j, graph)

            truck.route[0] = create_route(truck.route[2], graph, previous_stop)

            # recurse I guess?
            execute_route(truck, graph)
            return

        next_stop = truck.route[0][i]

        stop_distance += graph.get_weight(next_stop[1], previous_stop[1])

        while distance_traveled <= stop_distance:
            distance_traveled += speed_per_min
            traveled_miles += speed_per_min

            if sim:
                if distance_traveled >= stop_distance:
                    break

                time.sleep(interval)
            else:
                # Do the stuff for not simulation. Check the time and such
                pass

        # Mark the packages as delivered
        deliv_time = get_sim_time()

        for j in next_stop[2:]:
            for k in truck.packages:
                if k.get("Package ID") == j and k not in wrong_address_packages:
                    if type(k.get("Delivery Deadline")) == str or k.get("Delivery Deadline") >= deliv_time:
                        k.set("Delivery Status", f"Package Delivered at {deliv_time}")
                        truck.packages.remove(k)
                        truck.route[2].remove(j)
                    elif k.get("Delivery Deadline") < deliv_time:
                        k.set("Delivery Status", f"Package Delivered at {deliv_time} ***LATE***")
                        truck.packages.remove(k)
                        truck.route[2].remove(j)
                    break

        # Clear the variables that we have here
        previous_stop = next_stop


def main():
    global all_packages, sim, shutdown, complete, over_miles, delayed, paired, time_critical, wrong_address

    # Define our trucks
    total_trucks = 3
    trucks = [Truck(i + 1) for i in range(total_trucks)]

    # Simulation variable, False, follows true time of day, True, 1 minute = 1 second
    sim = True

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
                stop_map.add_edge(distances_headers.iloc[j].replace('\n', ' '), row[0], row[j])  # Add the reverse edge

    # filter some stuff
    size = all_packages.size()
    truck_specific = []

    # Create our trucks
    for i in range(total_trucks):
        truck_specific.append([])

    # Add our packages to categories
    for i in range(1, size + 1):
        curr_pack = all_packages.get_package(i)

        if type(curr_pack.get("Delivery Deadline")) is not str:  # Delivered by a specific time?
            time_critical.append(curr_pack.get("Package ID"))

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

        new_label.append(pack_id)

        stop_map.update_vertex(address, new_label)

    # Create the routes
    max_miles = 140  # Per project requirements (for all trucks combined)

    # Generate every possible route? No sir
    possible_routes = HashIt()

    for i in stop_map.labels:
        packages = []
        new_route = []
        length = 0

        if "HUB" not in i[1]:
            new_route.append(stop_map.labels[0])
            new_route.append(i)

            # Set initial length from hub to first stop
            length += stop_map.get_weight(stop_map.labels[0][1], i[1])

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

    # find a route that matches paired out of the ideal efficient routes or has at least 75% of the packages
    paired_routes = []
    paired_routes_final = []

    for i in paired:
        for j in stop_map.labels:
            if "HUB" not in j[1] and (i in possible_routes.get(j[1])[2] or len(list(set(i).intersection(possible_routes.get(j[1])[2]))) >= len(i) * .70):
                paired_routes.append(possible_routes.get(j[1]))

    # Find the most efficient out of the paired routes, save them if 70% of packages match:
    for i in paired:
        efficient = None

        for j in paired_routes:
            if efficient is None and i != []:
                efficient = j
            elif len(list(set(i).intersection(j[2]))) >= len(list(set(i).intersection(efficient[2]))):
                efficient = j

        if efficient is not None:
            paired_routes_final.append(efficient)

    # Check to see if there's one route or multiple
    paired_routes_final = shortest_route(paired_routes_final, stop_map)

    # Add any missing packages
    # TODO: THis will need to be handled better too refer to note below for the too part
    paired_routes_final[2] += paired[0]
    new_pack = [*set(paired_routes_final[2])]
    new_pack.sort()
    paired_routes_final = [create_route(new_pack, stop_map), 0, new_pack]
    paired_routes_final[1] = distance_calc(paired_routes_final[0], stop_map)

    # Find a route that matches truck requirements
    truck_specific_routes = []
    truck_specific_routes_final = []

    for i in truck_specific:
        if len(i) != 0:
            for j in stop_map.labels:
                if "HUB" not in j[1] and (i in possible_routes.get(j[1])[2] or len(list(set(i).intersection(possible_routes.get(j[1])[2]))) > len(i) * .70):
                    truck_specific_routes.append(possible_routes.get(j[1]))

    # Find the most efficient out of the truck specific, save them if 70% of packages match:
    for i in truck_specific:
        efficient = None

        for j in truck_specific_routes:
            if not i:
                break

            if efficient is None:
                efficient = j
            elif len(list(set(i).intersection(j[2]))) > len(list(set(i).intersection(efficient[2]))):
                efficient = j

        if efficient is not None:
            truck_specific_routes_final.append(efficient)

    # TODO: Need to handle this a bit differently. This will create issues if there are multiple trucks with requirements
    truck_specific_routes_final = shortest_route(truck_specific_routes_final, stop_map)

    # Add any missing packages
    truck_specific_routes_final[2] += truck_specific[1]
    new_pack = [*set(truck_specific_routes_final[2])]
    new_pack.sort()
    truck_specific_routes_final = [create_route(new_pack, stop_map), 0, new_pack]
    truck_specific_routes_final[1] = distance_calc(truck_specific_routes_final[0], stop_map)

    # Find a route that matches delayed flights
    delayed_route = [create_route(delayed, stop_map), 0, delayed]
    delayed_route[1] = distance_calc(delayed_route[0], stop_map)

    # make sure each package is only making it on one truck
    undelivered = list(range(1, all_packages.size() + 1))
    on_routes = delayed + truck_specific_routes_final[2] + paired_routes_final[2]
    on_routes = [*set(on_routes)]

    undelivered = list(set(undelivered).difference(set(on_routes)))

    """
    Hierarchy:
    Delayed
    Truck_specific
    Paired
    """

    # Delayed Checks
    if len(set(delayed_route[2]).intersection(set(truck_specific_routes_final[2]))) != 0:
        truck_specific_routes_final[2] = [*set(truck_specific_routes_final[2]).difference(delayed_route[2])]
        truck_specific_routes_final[0] = create_route(truck_specific_routes_final[2], stop_map)
        truck_specific_routes_final[1] = distance_calc(truck_specific_routes_final[0], stop_map)
    if len(set(delayed_route[2]).intersection(set(paired_routes_final[2]))) != 0:
        paired_routes_final[2] = [*set(paired_routes_final[2]).difference(delayed_route[2])]
        paired_routes_final[0] = create_route(paired_routes_final[2], stop_map)
        paired_routes_final[1] = distance_calc(paired_routes_final[0], stop_map)

    # Truck Specific Checks. Paired should all be good after this point theoretically
    if len(set(truck_specific_routes_final[2]).intersection(set(paired_routes_final[2]))) != 0:
        paired_routes_final[2] = [*set(paired_routes_final[2]).difference(truck_specific_routes_final[2])]
        paired_routes_final[0] = create_route(paired_routes_final[2], stop_map)
        paired_routes_final[1] = distance_calc(paired_routes_final[0], stop_map)

    # Add missed packages to smaller routes or create their own
    finalized_routes = [paired_routes_final, truck_specific_routes_final, delayed_route]
    temp_routes = copy.deepcopy(finalized_routes)
    new_undelivered = copy.deepcopy(undelivered)

    # First try to add to existing routes
    for i in undelivered:
        most_efficient_route = None
        added_routes = []

        for j in temp_routes:
            j[2].append(i)
            added_routes.append([create_route(j[2], stop_map), distance_calc(create_route(j[2], stop_map), stop_map), j[2]])

        for j in range(len(added_routes)):
            if (not most_efficient_route or added_routes[j][1] < added_routes[most_efficient_route][1]) and len(added_routes[j][2]) <= 16:
                most_efficient_route = j

        if most_efficient_route is not None:
            finalized_routes[most_efficient_route] = copy.deepcopy(added_routes[most_efficient_route])
            new_undelivered.remove(i)

    undelivered = new_undelivered

    # Make a route with the remaining
    if len(undelivered) > 0:
        pass  # Do something eventually maybe a new route

    # make sure we are good on our miles
    if finalized_routes[0][1] + finalized_routes[1][1] + finalized_routes[2][1] < max_miles:
        print("YES WE ARE GOOD ON MILES")
    else:
        print("DAMN IT *Schmidt impersonation*")
        over_miles = True

    # Change the status of each package, start with truck specific
    for i in finalized_routes:
        for j in range(total_trucks):
            if len(set(i[2]).intersection(set(truck_specific[j]))) > 0 and len(trucks[j].packages) == 0:
                trucks[j].route = i

                for k in i[2]:
                    trucks[j].add_package(all_packages.get_package(k))
                    all_packages.get_package(k).set("Delivery Status", f"Package is on truck {trucks[j].truck_id} for delivery")

                    if trucks[j].departure_time == math.inf:
                        trucks[j].departure_time = datetime.time(8)
                break
            elif len(trucks[j].packages) == 0:
                for k in i[2]:
                    if type(all_packages.get_package(k).get("Special Note")) != str or 'Delayed' not in all_packages.get_package(k).get("Special Note"):
                        trucks[j].route = i
                        trucks[j].add_package(all_packages.get_package(k))
                        all_packages.get_package(k).set("Delivery Status", f"Package is on truck {trucks[j].truck_id} for delivery")

                        if trucks[j].departure_time == math.inf:
                            trucks[j].departure_time = datetime.time(8)
                    else:
                        trucks[j].route = i
                        trucks[j].add_package(all_packages.get_package(k))
                        all_packages.get_package(k).set("Delivery Status", f"truck {trucks[j].truck_id} waiting for arrival")

                        if trucks[j].departure_time == math.inf or trucks[j].departure_time < datetime.time(9, 5):
                            trucks[j].departure_time = datetime.time(9, 5)
                break

    # start our timer
    if sim:
        Thread(target=sim_time, args=(1,)).start()

    starting_threads = threading.active_count()

    # Do a last minute calculation, execute the routes
    for i in trucks:
        i.route[0] = create_route(i.route[2], stop_map)
        Thread(target=execute_route, args=(i, stop_map)).start()

    # TODO: Create new threads for other routes if needed

    # Loop until threads are done
    while threading.active_count() > starting_threads:
        time.sleep(interval)

    # Make sure all packages are delivered
    for i in trucks:
        if len(i.packages) > 0:
            i.route[0] = create_route(i.route[2], stop_map)
            execute_route(i, stop_map)
            # Thread(target=execute_route, args=(i, stop_map)).start()

    complete = True


if __name__ == "__main__":
    threading.Thread(target=main).start()
    time.sleep(1)
    create_package_table()


"""
Some thoughts:

When inevitably redoing the create route function, add the array's into it.

Create a list of time critical
Start making routes based on them, divide them evenly by the amount of trucks maybe? take the ones that are delayed out and make a separate route
remove the time critical from the total list of packages
check the selected package for relation to other lists add those packages after the fact, drop second to last stop or however many is needed to get it under 16 packages
return the total amount of lists
"""