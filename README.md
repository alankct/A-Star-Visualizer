# Visualizing A* Search Algorithm

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