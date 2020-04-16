import java.awt.Point;
import java.util.ArrayList;
import java.util.List;
import java.util.Comparator;
import java.util.Collections;
import java.util.AbstractMap;
import java.util.HashMap;
import java.util.PriorityQueue;

public class Dijkstra implements AIModule
{
    /// Creates the path to the goal.
    public List<Point> createPath(final TerrainMap map)
    {

    // Initializing ArrayLists

            // Holds the resulting path
            final ArrayList<Point> path = new ArrayList<Point>();

            // TODO: USE PRIORITY QUEUE, MAKE SORT WORK

            // Holds the paths to be explored
            final PriorityQueue<Node> frontier = new PriorityQueue<Node>(new ComparatorClass());

        // Initialize all Nodes, create Hash Map for convenience
            final HashMap<Point, Node> graph = new HashMap<Point, Node>();
            Point nullPoint = new Point(-1,-1);
            double inf = Double.POSITIVE_INFINITY;
            for (int i=0; i < map.getWidth(); i++){
                for (int j=0; j < map.getHeight(); j++) {
                    Point k = new Point(i,j);
                    Node l = new Node(k,inf,nullPoint);
                    graph.put(k,l);
                }
            }

        // Create currentNode, initialize for start point
        Node currentNode = graph.get(map.getStartPoint());
        currentNode.setNodeCost(0.0);
        currentNode.setParent(map.getStartPoint());
        frontier.add(currentNode);

        // Main Loop
        while(true) {

            // Failure returns almost-empty path
            if(frontier.size()==0){
                break;
            }

            else {
               
               // Pop currentNode from frontier, initialize useful variables
                currentNode = frontier.poll();
                Point p = currentNode.getPoint();
                Point parent = currentNode.getParent();
                
                // Handle goal state
                if(map.getEndPoint().equals(p)) {
                    while (!map.getStartPoint().equals(p)) {
                        path.add(p);
                        currentNode = graph.get(p);
                        parent = currentNode.getParent();
                        p = parent;
                    }
                    path.add(map.getStartPoint());
                    Collections.reverse(path);
                    break;
                }

                // Iterate through neighbors
                Point[] n = map.getNeighbors(p);
                for(Point l : n) {
                    Point n1 = l;
                    if (map.validTile(n1)) {
                        Node nNode = graph.get(n1);
                        Double newCost = currentNode.getNodeCost() + map.getCost(p,n1);
                        if (newCost < nNode.getNodeCost()) {
                            nNode.setNodeCost(newCost);
                            nNode.setParent(p);
                            graph.replace(n1,nNode);
                            frontier.add(nNode);
                    }
                    }
                }
            }
    }
    //System.out.println(path);
    return path;
}

    // Create Node Class
    private class Node { 
    Node(Point p2, Double cost2, Point parent2){
        p = p2;
        cost = cost2;
        parent = parent2;
        } 
        public void setNodeCost(Double cost3) {
            cost = cost3;
        }
        public void setParent(Point parent3){
            parent = parent3;
        }
        public Point getPoint() {
            return p;
        }
        public Double getNodeCost() {
            return cost;
        }
        public Point getParent() {
            return parent;
        }
        final private Point p;
        private Double cost;
        private Point parent;
    }   

    // Comparator Class for use in Priority Queue
    class ComparatorClass implements Comparator<Node> {
        public int compare (Node n1, Node n2) {
            if (n1.getNodeCost() < n2.getNodeCost()) return -1;
            if (n1.getNodeCost() > n2.getNodeCost()) return 1;
            return 0;
        }
    }
}

