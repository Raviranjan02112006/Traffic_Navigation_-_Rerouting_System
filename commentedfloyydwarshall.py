# Import required libraries
import tkinter as tk  # For GUI development
from tkinter import ttk, messagebox  # For advanced GUI components and error messages
import matplotlib.pyplot as plt  # For graph visualization
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # To embed matplotlib plots in tkinter
import networkx as nx  # For graph creation and manipulation

# Class to represent a traffic navigation system using a graph
class TrafficGraph:
    def __init__(self):
        # Initialize the graph as a dictionary and an empty set of nodes
        self.graph = {}
        self.nodes = set()

    # Method to add a road (edge) between two nodes in the graph
    def add_road(self, from_node, to_node, weight):
        # Add an edge from `from_node` to `to_node` with a given weight (distance)
        self.graph.setdefault(from_node, []).append((to_node, weight))
        # Since this is an undirected graph, also add the reverse edge
        self.graph.setdefault(to_node, []).append((from_node, weight))
        # Add the nodes to the set of all nodes
        self.nodes.add(from_node)
        self.nodes.add(to_node)

    # Method to create an adjacency matrix for the graph
    def create_adjacency_matrix(self):
        # Initialize the adjacency matrix with all distances set to infinity
        adj_matrix = {node: {node2: float('infinity') for node2 in self.nodes} for node in self.nodes}
        # Set the diagonal to 0 (distance from a node to itself is 0)
        for node in self.nodes:
            adj_matrix[node][node] = 0
        # Update the adjacency matrix with the actual edge weights from the graph
        for node in self.graph:
            for neighbor, weight in self.graph[node]:
                adj_matrix[node][neighbor] = weight
        return adj_matrix

    # Method to implement the Floyd-Warshall algorithm
    def floyd_warshall(self):
        # Get the initial adjacency matrix
        dist = self.create_adjacency_matrix()
        # Update the matrix to calculate the shortest paths
        for k in self.nodes:  # Intermediate node
            for i in self.nodes:  # Start node
                for j in self.nodes:  # End node
                    # Update the shortest distance between i and j using node k as an intermediary
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist

# Function to plot the graph using matplotlib and NetworkX
def plot_graph(graph):
    plt.clf()  # Clear the current figure
    G = nx.Graph()  # Create an undirected graph object

    # Add edges and weights to the graph
    for node in graph:
        for neighbor, weight in graph[node]:
            G.add_edge(node, neighbor, weight=weight)

    # Generate positions for the nodes
    pos = nx.spring_layout(G)

    # Set figure size
    plt.figure(figsize=(10, 8))

    # Draw the graph with labels, colors, and edge weights
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    plt.title('Enhanced Traffic Navigation System')

    # Embed the graph into the tkinter window
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()  # Destroy the old canvas if it exists
    canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to display a matrix (e.g., adjacency or Floyd-Warshall result)
def display_matrix(matrix, title):
    # Update the result label with the matrix in a readable format
    result_label.config(text=f"{title}:\n" + '\n'.join([f"{node}: {dict(values)}" for node, values in matrix.items()]))

# Main function to set up the GUI and traffic navigation system
def main():
    global window, canvas, result_label  # Declare global variables
    traffic_graph, canvas = TrafficGraph(), None  # Create a TrafficGraph object

    # Pre-defined map of Delhi with 15 locations and roads (edges) between them
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

    # Add the predefined roads to the traffic graph
    for road in delhi_locations:
        traffic_graph.add_road(road[0], road[1], road[2])

    # Function to add a new road
    def add_road():
        from_node, to_node, weight = from_node_var.get(), to_node_var.get(), int(weight_var.get())
        if not from_node or not to_node or weight <= 0:
            messagebox.showerror("Error", "Invalid input. Please enter valid node names and a positive weight.")
            return
        traffic_graph.add_road(from_node, to_node, weight)  # Add the road
        plot_graph(traffic_graph.graph)  # Update the graph plot
        messagebox.showinfo("Success", f"Road added: {from_node} -> {to_node} with distance {weight} units")

    # Function to show the adjacency matrix
    def show_adjacency_matrix():
        adj_matrix = traffic_graph.create_adjacency_matrix()
        display_matrix(adj_matrix, "Adjacency Matrix")

    # Function to show Floyd-Warshall results
    def show_floyd_warshall_results():
        fw_matrix = traffic_graph.floyd_warshall()
        display_matrix(fw_matrix, "Floyd-Warshall Shortest Paths")

    # Create the main tkinter window
    window = tk.Tk()
    window.title("Enhanced Traffic Navigation System")
    window.geometry("1000x800")

    # Input fields for adding roads
    from_node_var = tk.StringVar()
    to_node_var = tk.StringVar()
    weight_var = tk.StringVar()

    # GUI components for adding a road
    ttk.Label(window, text="Add Roads (Edges)").pack(pady=5)
    ttk.Label(window, text="From:").pack(pady=2)
    ttk.Entry(window, textvariable=from_node_var).pack(pady=2)
    ttk.Label(window, text="To:").pack(pady=2)
    ttk.Entry(window, textvariable=to_node_var).pack(pady=2)
    ttk.Label(window, text="Distance (Weight):").pack(pady=2)
    ttk.Entry(window, textvariable=weight_var).pack(pady=2)
    ttk.Button(window, text="Add Road", command=add_road).pack(pady=5)

    # Buttons to show the adjacency matrix and Floyd-Warshall results
    ttk.Button(window, text="Show Adjacency Matrix", command=show_adjacency_matrix).pack(pady=10)
    ttk.Button(window, text="Show Floyd-Warshall Results", command=show_floyd_warshall_results).pack(pady=10)

    # Label to display results (matrix outputs)
    result_label = ttk.Label(window, text="", wraplength=900)
    result_label.pack(pady=10)

    # Plot the initial graph
    plot_graph(traffic_graph.graph)

    # Run the tkinter event loop
    window.mainloop()

# Entry point for the program
if __name__ == "__main__":
    main()