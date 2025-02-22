ABSTRACT:
The project "Traffic Navigation and Rerouting System" aims to develop an intelligent solution for navigating city traffic and dynamically rerouting vehicles based on road conditions. This system integrates graph-based algorithms to model a traffic network, where roads and intersections are represented as nodes and edges with associated weights. Utilizing Dijkstra's algorithm for shortest path calculation and the Floyd-Warshall algorithm for all-pairs shortest paths, the system identifies the most efficient routes between user-selected points.
The system features a user-friendly GUI built with tkinter, allowing users to input traffic conditions such as "Rush Hour" or "Accident Zone" to simulate real-time congestion. Predefined locations within Delhi are used to create a realistic traffic simulation. The application enables route visualization and updates travel times dynamically, providing alternative routes in the case of heavy traffic. Through the use of algorithms and traffic data simulation, the project seeks to reduce travel times and enhance urban mobility.
The sample data of 15 congested places of Delhi - NCR region has been taken in the intial map. While more roads can be added by the users conmnecting any of  15 places taken in sample in the GUI of both Dijkstra Algorithm And Floyyd Warshall Algorithm.

CONCLUSION:
For Traffic Navigation: Dijkstra's Algorithm is more efficient for applications needing quick, single-source shortest path calculations. Such as individual route planning or dynamic rerouting based on traffic conditions.
For Comprehensive Mapping and Static Systems: Floyd-Warshall Algorithm is more suited for static systems requiring a detailed map of all shortest paths, such as pre-computed navigation systems and network analysis tools.
Additionally, Floyd-Warshall can be beneficial in scenarios where the navigation system needs to pre-calculate all possible routes to provide instant responses, while Dijkstra excels in scenarios requiring real-time data adaptation and lower memory usage.

FUTURE SCOPE:
Some of the future advancements for the proposed system may be:- 
-Real-Time Traffic Prediction and Adaptive Routing, 
-Integration with Autonomous Vehicles, 
-AI and Machine Learning Advancements,
-Crowdsourcing and Collaborative Systems
