import tkinter as tk  # Import tkinter for creating GUI applications
from tkinter import ttk, messagebox  # Import ttk for themed widgets and messagebox for dialog boxes
import heapq  # Import heapq to use the priority queue for Dijkstra's algorithm
import matplotlib.pyplot as plt  # Import matplotlib for plotting graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import to embed matplotlib graphs into tkinter window
import networkx as nx  # Import NetworkX for graph-related operations

# Class to represent a traffic graph
class TrafficGraph:
    def __init__(self):
        self.graph = {}  # Initialize an empty graph as a dictionary

    # Method to add roads (edges) between nodes in the graph
    def add_road(self, from_node, to_node, weight):
        # Add the road with its weight (distance) between two nodes
        self.graph.setdefault(from_node, []).append((to_node, weight))
        self.graph.setdefault(to_node, []).append((from_node, weight))

    # Dijkstra's algorithm to find the shortest path between two nodes
    def dijkstra(self, start, end):
        pq = [(0, start)]  # Priority queue to store (distance, node) pairs, starting with (0, start)
        distances = {node: float('infinity') for node in self.graph}  # Initialize all node distances to infinity
        distances[start] = 0  # Distance to the start node is zero
        previous_nodes = {node: None for node in self.graph}  # Store the previous nodes to reconstruct the path

        # While there are nodes in the priority queue
        while pq:
            current_distance, current_node = heapq.heappop(pq)  # Get the node with the smallest distance
            if current_node == end:
                break  # If the destination is reached, break out of the loop
            for neighbor, weight in self.graph[current_node]:
                distance = current_distance + weight  # Calculate the new distance to the neighboring node
                if distance < distances[neighbor]:  # If the new distance is smaller, update it
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node  # Track the previous node for path reconstruction
                    heapq.heappush(pq, (distance, neighbor))  # Push the new distance to the priority queue

        # Reconstruct the path from end to start
        path, current_node = [], end
        while current_node:
            path.append(current_node)
            current_node = previous_nodes[current_node]
        return path[::-1], distances[end] if distances[end] != float('infinity') else None  # Return reversed path and distance

    # Recursive method to find all possible paths between two nodes
    def get_all_paths(self, start, end, path=[], all_paths=[]):
        path = path + [start]  # Add the starting node to the path
        if start == end:  # If the start is the end, a path is found
            all_paths.append(path)  # Append the path to all_paths
        elif start in self.graph:  # If the start node is in the graph, continue searching
            for node, _ in self.graph[start]:
                if node not in path:  # Avoid cycles by checking if the node is already in the path
                    self.get_all_paths(node, end, path, all_paths)  # Recursively find paths
        return all_paths  # Return all found paths

# Function to plot the traffic graph and highlight the shortest path if provided
def plot_graph(graph, path=None):
    plt.clf()  # Clear the current figure to avoid overlapping plots
    G = nx.Graph()  # Create a new graph using NetworkX
    for node in graph:
        for neighbor, weight in graph[node]:
            G.add_edge(node, neighbor, weight=weight)  # Add edges with weights to the NetworkX graph
    pos = nx.spring_layout(G)  # Use a layout to position nodes in the graph
    plt.figure(figsize=(10, 8)) 
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=12)  # Draw the graph
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))  # Label edges with their weights
    if path:
        nx.draw_networkx_edges(G, pos, edgelist=list(zip(path, path[1:])), edge_color='red', width=3)  # Highlight the path in red
    plt.title('Traffic Navigation System')  # Set the title of the plot
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()  # Remove the old plot from the GUI
    canvas = FigureCanvasTkAgg(plt.gcf(), master=window)  # Embed the new plot in the tkinter window
    canvas.draw()  # Draw the plot
    canvas.get_tk_widget().pack()  # Pack the canvas into the window

# Main function to set up the tkinter GUI and handle user inputs
def main():
    global window, canvas
    traffic_graph, canvas = TrafficGraph(), None  # Create a new TrafficGraph object and initialize canvas

    # Pre-create the map with 15 locations and roads (edges) between them
    delhi_locations = [
    ("Connaught Place", "Chandni Chowk", 5), ("Connaught Place", "Karol Bagh", 4),
    ("Connaught Place", "Lajpat Nagar", 7), ("Connaught Place", "Hauz Khas", 10),
    ("Chandni Chowk", "Karol Bagh", 6), ("Chandni Chowk", "Shahdara", 8),
    ("Karol Bagh", "Rohini", 12), ("Karol Bagh", "Pitampura", 10),
    ("Lajpat Nagar", "Saket", 5), ("Lajpat Nagar", "Greater Kailash", 4),
    ("Saket", "Hauz Khas", 3), ("Hauz Khas", "Vasant Kunj", 6),
    ("Vasant Kunj", "Dwarka", 15), ("Dwarka", "Janakpuri", 8),
    ("Janakpuri", "Pitampura", 18), ("Pitampura", "Shahdara", 20),
    ("Shahdara", "Noida", 12), ("Noida", "Mayur Vihar", 5),
    ("Mayur Vihar", "Greater Kailash", 10), ("Greater Kailash", "Hauz Khas", 8)
]

    
    # Add predefined roads to the graph
    for road in delhi_locations:
        traffic_graph.add_road(road[0], road[1], road[2])


    # Function to add roads (edges) to the graph
    def add_road():
        from_node, to_node, weight = from_node_var.get(), to_node_var.get(), int(weight_var.get())  # Get input values
        if not from_node or not to_node or weight <= 0:  # Validate inputs
            messagebox.showerror("Error", "Invalid input. Please enter valid node names and a positive weight.")  # Show error
            return
        traffic_graph.add_road(from_node, to_node, weight)  # Add the road to the graph
        plot_graph(traffic_graph.graph)  # Plot the updated graph
        messagebox.showinfo("Success", f"Road added: {from_node} -> {to_node} with distance {weight} units")  # Show success

    # Function to find and display the shortest route between two points
    def find_route():
        start, end, vehicle_speed = start_var.get(), end_var.get(), float(speed_var.get())  # Get inputs
        if start not in traffic_graph.graph or end not in traffic_graph.graph:  # Validate inputs
            messagebox.showerror("Error", "Invalid starting or destination point.")  # Show error
            return
        path, distance = traffic_graph.dijkstra(start, end)  # Find the shortest path using Dijkstra's algorithm
        if path and distance is not None:
            travel_time = distance / vehicle_speed  # Calculate estimated travel time
            result_label.config(text=f"Route: {' -> '.join(path)}\nTotal Distance: {distance} units\nEstimated Time: {travel_time:.2f} hours")  # Display results
            plot_graph(traffic_graph.graph, path)  # Plot the graph with the shortest path highlighted
        else:
            result_label.config(text="No route found.")  # Show error if no path is found

    # Function to find and display all alternative routes between two points
    def find_alternative_routes():
        start, end = start_var.get(), end_var.get()  # Get inputs
        if start not in traffic_graph.graph or end not in traffic_graph.graph:  # Validate inputs
            messagebox.showerror("Error", "Invalid starting or destination point.")  # Show error
            return
        all_paths = traffic_graph.get_all_paths(start, end)  # Find all paths between the two nodes
        result_text = "Alternative Routes:\n" + '\n'.join([' -> '.join(path) for path in all_paths]) if all_paths else "No alternative routes found."  # Format results
        result_label.config(text=result_text)  # Display results

    # Function to simulate traffic conditions and update the travel time
    def simulate_and_update_traffic():
        start, end, vehicle_speed = start_var.get(), end_var.get(), float(speed_var.get())  # Get inputs
        if start not in traffic_graph.graph or end not in traffic_graph.graph:  # Validate inputs
            messagebox.showerror("Error", "Invalid starting or destination point.")  # Show error
            return

        # Congestion factor based on traffic condition
        congestion_factor = 1.0
        if traffic_condition_var.get() == "Rush Hour":
            congestion_factor = 1.5
        elif traffic_condition_var.get() == "Accident Zone":
            congestion_factor = 2.0

        path, distance = traffic_graph.dijkstra(start, end)  # Find the shortest path using Dijkstra's algorithm
        if path and distance is not None:
            # Adjust travel time based on congestion factor
            adjusted_travel_time = (distance / vehicle_speed) * congestion_factor
            result_label.config(text=f"Route: {' -> '.join(path)}\nTotal Distance: {distance} units\nAdjusted Travel Time: {adjusted_travel_time:.2f} hours")  # Display results
            plot_graph(traffic_graph.graph, path)  # Plot the graph with the shortest path highlighted
        else:
            result_label.config(text="No route found.")  # Show error if no path is found

    # Initialize the main window
    window = tk.Tk()
    window.title("Traffic Navigation and Rerouting System")
    window.geometry("800x600")

    # Input fields and labels for adding roads
    from_node_var, to_node_var, weight_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
    ttk.Label(window, text="Add Roads (Edges)").pack(pady=5)
    tk.Label(window, text="From").pack(pady=2)
    tk.Entry(window, textvariable=from_node_var).pack(pady=2)
    tk.Label(window, text="To").pack(pady=2)
    tk.Entry(window, textvariable=to_node_var).pack(pady=2)
    tk.Label(window, text="Distance (Weight)").pack(pady=2)
    tk.Entry(window, textvariable=weight_var).pack(pady=2)
    tk.Button(window, text="Add Road", command=add_road).pack(pady=5)

    # Input fields and labels for finding routes
    start_var, end_var, speed_var = tk.StringVar(), tk.StringVar(), tk.StringVar(value="40")  # Default speed is 40 units/hour
    tk.Label(window, text=" Select Starting Point").pack(pady=5)
    tk.Entry(window, textvariable=start_var).pack(pady=5)
    tk.Label(window, text="Select Destination Point").pack(pady=5)
    tk.Entry(window, textvariable=end_var).pack(pady=5)
    tk.Label(window, text="Vehicle Speed (units/hour)").pack(pady=5)
    tk.Entry(window, textvariable=speed_var).pack(pady=2)
    tk.Button(window, text="Find Route", command=find_route).pack(pady=10)
    tk.Button(window, text="Find Alternative Routes", command=find_alternative_routes).pack(pady=5)

    # Dropdown menu for traffic conditions
    traffic_condition_var = tk.StringVar()
    tk.Label(window, text="Traffic Condition").pack(pady=5)
    ttk.Combobox(window, textvariable=traffic_condition_var, values=["Normal", "Rush Hour", "Accident Zone"], state="readonly").pack(pady=2)

    # Buttons to find routes and simulate traffic
    
    tk.Button(window, text="Simulate Traffic", command=simulate_and_update_traffic).pack(pady=5)

    # Label to display results
    result_label = tk.Label(window, text="", wraplength=900)
    result_label.pack(pady=10)

    plot_graph(traffic_graph.graph)  # Initial plot of the predefined graph

    window.mainloop()  # Start the tkinter main loop

if __name__ == "__main__":
    main()
