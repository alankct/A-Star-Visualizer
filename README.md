# Visualizing A* Search Algorithm

> This project is an interactive visualization of A* Search (I got really into Search algorithms in the summer)

<h4>
   How to start: Given a grid (1st image), plot a start and end point (2nd image)
</h4>

<body>
    <p style="float: left;">
      <img width="396" height="396" alt="Screenshot 2023-11-14 at 12 28 12 PM" src="https://github.com/alankct/A-Star-Visualizer/assets/86837040/321a8e7f-3498-496b-b04e-442d72262ad6">
      <img width="396" height="396" alt="Screenshot 2023-11-14 at 12 28 49 PM" src="https://github.com/alankct/A-Star-Visualizer/assets/86837040/05866a96-1f84-4e1c-a14b-79b0e5e355c9">
      <h4>
         To play: Place your obstacles (3rd image), and press space to visualize the A* algorithm in action (4th image) 
      </h4>
      <img width="396" height="396" alt="Screenshot 2023-11-14 at 12 37 36 PM" src="https://github.com/alankct/A-Star-Visualizer/assets/86837040/478de2e6-e817-4d40-b63b-9776d330664e">
      <img width="396" height="396" alt="Screenshot 2023-11-14 at 12 38 47 PM" src="https://github.com/alankct/A-Star-Visualizer/assets/86837040/cdf13b28-1c2c-4def-aa99-b30ae49147da">
    </p>
</body>

Pathfinding algorithms seek to find the shortest path between points A and B. 
This program visualizes the **A-Star pathfinding algorithm** in action, into a 2D grid, where movements
from one node to another (up, down, left or right) have a _cost_ of 1.

A-Star Search is arguably the best pathfinding algorithm; it uses heuristics to guarantee the shortest
path much faster than Dijkstra's Algorithm.

At each iteration of its main loop, A* figures out which of its paths to extend. It does so based
on the cost of a path and the estimated cost required to extend this path all the way to the goal. 

**Specifically, A-Star selects the path that minimizes f(n)=g(n)+h(n)**

... where **n** is the next node on the path, **g(n)** is the cost of the path from the start node to n, 
and **h(n)** is a heuristic function that estimates the cost of the direct path from n to the goal.

In the worst case, the A-star algorithm travels all the edges to reach Point B from Point A. So the
worse case time complexity is O(VlogV) — where V is the number of vertices in the graph — since it
implements a Priority Queue to figure out which node to progress next. 

Further, in the worse case, we can have all the edges inside the open list Priority Queue, so the
required extra space in the worst case is O(V), where V is the total number of vertices.

The space complexity of A* is roughly the same as that of all other graph search algorithms, as it
keeps all generated nodes in memory. In practice, this turns out to be the biggest drawback of A*
search, leading to the development of memory-bounded heuristic searches, such as Iterative deepening
A*, memory bounded A*, and SMA*.
