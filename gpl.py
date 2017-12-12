#
# My Graph Library implementation in Python
#
# Georg Prohaska h0325904@wu.ac.at
#
# How to run: `python gpl.py`
#
#
# Prerequisites
#


import unittest
import queue
from operator import methodcaller
import copy
import math

class Base():
  #
  # Begin of my implementation
  # ---------------%<------------------

  
    class Node:
        def __init__(self):
            self._neighbours = []
            
        def neighbours(self):
            return self._neighbours
            
        def addNeighbour(self, neighbour):
            self._neighbours.append(neighbour)
            
        def addNeighbours(self, neighbours):
            self._neighbours.extend(neighbours)
            
    class Neighbour:
        def __init__(self, opposite):
            self._opposite = opposite
            
        def opposite(self):
            return self._opposite
        
    class WeightedNeighbour(Neighbour):
        def __init__(self, opposite, weight):
            super().__init__(opposite)
            self._weight = weight                  
            
        def weight(self):
            return self._weight
        
    class Edge:
        def __init__(self, node1, node2):
            self._node1 = node1
            self._node2 = node2

        def node1(self):
            return self._node1
        def node2(self):
            return self._node2
        
    class WeightedEdge(Edge):
        def __init__(self, node1, node2, weight):
            super().__init__(node1, node2)
            self._weight = weight
            
        def weight(self):
            return self._weight

    class GraphException(Exception):
        pass

    #Manages the apropriate data structure (queue and stack) for BFS/DFS graph traversal
    class TraversalStore():
        def __init__(self, traversalMode):
            if traversalMode == Base.Graph.BFS:
                self._traversal = Base.Graph.BFS
                self._queue = queue.Queue()
            elif traversalMode == Base.Graph.DFS:
                self._traversal = Base.Graph.DFS
                self._stack = []
            else:
                raise Base.GraphException('Unknown traversal mode!')
            
        def traversalMode(self):
            return self._traversal

        #add an item to the store
        def add(self, item):
            if self._traversal == Base.Graph.BFS:
                self._queue.put(item)
            elif self._traversal == Base.Graph.DFS:
                self._stack.append(item)

        #gets and removes the item from the store
        def get(self):
            if self._traversal == Base.Graph.BFS:
                return self._queue.get()
            elif self._traversal == Base.Graph.DFS:
                return self._stack.pop()

        #checks wether store is empty
        def empty(self):
            if self._traversal == Base.Graph.BFS:
                return self._queue.empty()
            elif self._traversal == Base.Graph.DFS:
                if len(self._stack) == 0:
                    return True
                else:
                    return False
        #returns a list of all items in the stack
        def all(self):
            if self._traversal == Base.Graph.BFS:
                cp = copy.copy(self._queue)
                lst = list()
                while not cp.empty():
                    lst.append(cp.get())
                return lst
            else:
                return list(self._stack)

    class Graph():
        # "Constants"
        NEIGHBOUR = "neighbour"
        EDGE = "edge"
        BFS = "bfs"
        DFS = "dfs"

        def __init__(self, directed: bool = False, representation = None, weighted: bool = False, printable: bool = True, traversal = None, MST: bool = False, SSSP: bool = False):
            #Edge representation is the default
            if (representation == None) or (representation != Base.Graph.NEIGHBOUR):
                self._representation = Base.Graph.EDGE
                self._edges = []
            else:
                self._representation = representation
            
            self._directed = directed
            self._weighted = weighted
            self._printable = printable

            #default is not traversable
            if traversal == Base.Graph.BFS:
                self._traversal = Base.Graph.BFS
            elif traversal == Base.Graph.DFS:
                self._traversal = Base.Graph.DFS
            else:
                self._traversal = None

            #defaul is False
            if MST == True:
                if not self._weighted or self._directed:
                    raise Base.GraphException('MST only available for undirected, weighted graphs!')
                self._MST = True
            else:
                self._MST = False
            self._nodes = []                    
            #defazlt uis False
            if SSSP == True:
                if not self._weighted or not self._directed:
                    raise Base.GraphException('SSSP only available for directed, weighted graphs!')
                self._SSSP = True
            else:
                self._SSSP = False
        
        def nodeID(self, node):
            return self._nodes.index(node)
        
        def edges(self):
            if self._representation == Base.Graph.EDGE:
                return self._edges
            elif self._representation == Base.Graph.NEIGHBOUR:
                edges = list()
                visited = list()    
                for node in self._nodes:
                    for neighbour in node.neighbours():
                        if neighbour.opposite() in visited: continue
                        if self._weighted:
                            newEdge = Base.WeightedEdge(node, neighbour.opposite(), neighbour.weight())
                        else:
                            newEdge = Base.Edge(node, neighbour.opposite())
                        edges.append(newEdge)
                        if not self._directed: visited.append(node)
                return edges

        #returns an edge object (the internal object if the graph-representatio is an edge-list) between node1 and node2, None if it does not exist
        def edge(self, node1, node2):
            if node1 not in self._nodes or node2 not in self._nodes:
                return None
            if self._representation == Base.Graph.NEIGHBOUR:
                for neighbour in node1.neighbours():
                    if neighbour.opposite() is node2:
                        if self._weighted:
                            return Base.WeightedEdge(node1, neighbour.opposite(), neighbour.weight())
                        else:
                            return Base.Edge(node1, neighbour.opposite())
                return None
            elif self._representation == Base.Graph.EDGE:
                for edge in self._edges:
                    if edge.node1() is node1 and edge.node2() is node2:
                        return edge
                    if not self._directed:
                        if edge.node1() is node2 and edge.node2() is node1:
                            return edge
                return None
            else:
                raise Base.GraphException('Unknown representation!')


        def nodes(self):
            return self._nodes
                        
        def representation(self):
            return self._representation
        
        def directed(self):
            return self._directed
        
        def weighted(self):
            return self._weighted
        
        def printable(self):
            return self._printable

        def traversal(self):
            return self._traversal

        def setTraversal(self, traversalMode):
            if traversalMode == Base.Graph.DFS:
                self._traversal = Base.Graph.DFS
            elif traversalMode == Base.Graph.BFS:
                self._traversal= Base.Graph.BFS
            else:
                self._traversal = None

        #add an edge
        #in digraphs the direction is from m to n
        #positive weights are expected for weighted graphs
        def add(self, m, n, weight = None):
            if self._weighted == True:
                if weight == None or weight < 0:
                    raise Base.GraphException('Expected non-negative weight')
            #use different method for neighbour representation
            if self._representation == Base.Graph.NEIGHBOUR:
                return self._addNeighbourEdge(m, n, weight)
            # check if edge already exists
            for edge in self._edges:
                if edge.node1() is m and edge.node2() is n:
                    return edge
                if not self._directed:
                    if edge.node1() is n and edge.node2() is m:
                        return edge
                
            #add the new edge
            if self._weighted:
                e = Base.WeightedEdge(m, n, weight)
            else:
                e = Base.Edge(m, n)
            self._edges.append(e)              
            #add nodes
            self._addNode(m)
            self._addNode(n)
            return e
        
        #"private" method for adding edges in neighbour representation
        def _addNeighbourEdge(self, m, n, weight):
            #check if the object has an attribute called neighbours
            #(intentionally no Base.Node type check to make library more flexible)
            if not hasattr(m, "neighbours") or not hasattr(n, "neighbours"):
                raise TypeError("Expected a Node object")
            #check if edge already exists
            for neighbour in m.neighbours():
                if neighbour.opposite() is n:
                    self._addNode(m)
                    self._addNode(n)
                    return neighbour
            
            #add nodes
            self._addNode(m)
            self._addNode(n)
            #add neighbours
            mNeighbour = self._addNeighbour(m, n, weight)
                
            if not self._directed:
                self._addNeighbour(n, m, weight)
                
            return mNeighbour
            
        def _addNode(self, node):
            #only add nodes that do not exist in the graph yet
            if node not in self._nodes:
                self._nodes.append(node)
        
        #adds the correct type of neighbour object to the node
        def _addNeighbour(self, m, n, weight = None):
            #check if the object has a function to add neighbours 
            #(intentionally no Base.Node type check to make library more flexible)
            addNeighbourFunc = getattr(m, "addNeighbour", None)
            if not callable(addNeighbourFunc):
                raise TypeError("Expected a Node object")
                
            if self._weighted:
                mNeighbour = Base.WeightedNeighbour(n, weight)
                m.addNeighbour(mNeighbour)
            else:
                mNeighbour = Base.Neighbour(n)
                m.addNeighbour(mNeighbour)
            return mNeighbour
        
        def size(self):
            return len(self._nodes)
        
        def numEdges(self):
            if self._representation == Base.Graph.EDGE:
                return len(self._edges)
            elif self._representation == Base.Graph.NEIGHBOUR:
                edgeCounter = 0
                for node in self._nodes:
                    edgeCounter += len(node.neighbours())
                if not self._directed:
                    return edgeCounter / 2
                else:
                    return edgeCounter

        #DOT pretty printer
        def DOTprint(self):
            if not self._printable:
                raise Base.GraphException('Unprintable graph!')

            #start a graph
            if self._directed:
                DOTstring = 'digraph g{\nnode[label=""]; \n'
            else:
                DOTstring = 'graph g{\nnode[label=""]; \n'
            
            if self._representation == Base.Graph.EDGE:
                DOTstring += self._DOTedges()
            elif self._representation == Base.Graph.NEIGHBOUR:
                DOTstring += self._DOTneighbour()
            #finish graph
            DOTstring += "}"
            return DOTstring
                    
        #returns a string containing dot syntax of the edges in edge representation
        def _DOTedges(self):
            DOTstring = ""
            #add every edge
            for edge in self._edges:
                if self._weighted:
                    DOTstring += self._singleDOTedge(edge.node1(), edge.node2(), edge.weight())
                else:
                    DOTstring += self._singleDOTedge(edge.node1(), edge.node2())
            return DOTstring
        
        #returns a string containing dot syntax of the edges in neighbour representation
        def _DOTneighbour(self):
            DOTstring = ""
            visited = []
            for node in self._nodes:
                if self._directed:
                    for neighbour in node.neighbours():
                        if self._weighted:
                            DOTstring += self._singleDOTedge(
                                node, neighbour.opposite(), neighbour.weight())
                        else:
                            DOTstring += self._singleDOTedge(node, neighbour.opposite())
                        
                else:
                    for neighbour in node.neighbours():
                        if neighbour.opposite() in visited:
                            continue
                        if self._weighted:
                            DOTstring += self._singleDOTedge(
                                node, neighbour.opposite(), neighbour.weight())
                        else:
                            DOTstring += self._singleDOTedge(node, neighbour.opposite())

                visited.append(node)
                
            return DOTstring
        
        #returns the correct DOT representation for the current graph of a single edge
        #followed by a linebreak
        #a value for weight is expected for weighted graphs
        def _singleDOTedge(self, node1, node2, weight = None):
            edgeString = str(self.nodeID(node1))
            if self._directed:
                edgeString += " -> " 
            else:
                edgeString += " -- "
            edgeString += str(self.nodeID(node2))
            
            if self._weighted:
                edgeString += (" [ label = \"" + str(weight) + "\" ];")
            
            edgeString += "\n"
            return edgeString
        
        #uses the selected search algorithm to determine wether goalNode can be reached from startNode
        #throws GraphException if nodes are not part of the graph
        def search(self, startNode, goalNode):
            if self._traversal == None:
                raise Base.GraphException('Traversal mode currently turned off!')

            if (startNode not in self._nodes) or (goalNode not in self._nodes):
                raise Base.GraphException('Either start or goal are not part of this graph!')
            
            #initialise suitable data structure and add startNode
            visited = []
            store = Base.TraversalStore(self._traversal)
            store.add(startNode)
            visited.append(startNode)

            while not store.empty():
                node = store.get()
                if node is goalNode:
                    return True
                
                for neighbour in self.getNeighbourhood(node):
                    if neighbour not in visited:
                        store.add(neighbour)
                        visited.append(neighbour)
            return False

        #returns a list of all nodes that are adjacent to node
        def getNeighbourhood(self, node):
            if node not in self._nodes:
                raise Base.GraphException('Node not in graph!')

            neighbourhood = []
            if self._representation == Base.Graph.EDGE:
                for edge in self._edges:
                    if edge.node1() is node:
                        neighbourhood.append(edge.node2())    
                    elif edge.node2() is node:
                        #directed edges point from node1 to node2
                        if not self._directed:
                            neighbourhood.append(edge.node1())

            elif self._representation == Base.Graph.NEIGHBOUR:
                for neighbour in node.neighbours():
                    neighbourhood.append(neighbour.opposite())
            else:
                raise Base.GraphException('Unknown edge representation!')
            return neighbourhood

        #returns a Graph object containing the minimum spanning tree of this object, will throw an exception if Graphtype is wrong             
        def MST(self):
            if self._MST:
                alg = Base.MST(self)
                return alg.execute()
            else:
                raise Base.GraphException('MST disabled for this graph!')

        #returns a Graph object containing a directed tree rooted at the startnode. The edges represent the shortest path between the source and each node (weights stay the same)
        def SSSP(self, source):
            if self._SSSP:
                alg = Base.SSSP(self)
                return alg.execute(source)
            else:
                raise Base.GraphException('SSSP disabled for this graph!')
            
    #class for the MST algorithm, uses kruskals algorithm 
    class MST:
        def __init__(self, graph):
            if graph.directed() or not graph.weighted():
                raise Base.GraphException('MST works only for undirected weighted graphs')
            self._graph = graph
            self._parent = dict()
            self._rank = dict()

        def _makeSet(self, node):
            self._parent[node] = node
            self._rank[node] = 0

        def _find(self, node):
            if self._parent[node] != node:
                self._parent[node] = self._find(self._parent[node])
            return self._parent[node]

        def _union(self, node1, node2):
            root1 = self._find(node1)
            root2 = self._find(node2)

            if root1 == root2:
                return
                
            if self._rank[root1] < self._rank[root2]:
                self._parent[root1] = root2
            elif self._rank[root1] > self._rank[root2]:
                self._parent[root2] = root1
            else:
                self._parent[root2] = root1
                self._rank[root1] += 1 

        def execute(self):
            for node in self._graph.nodes():
                self._makeSet(node)
            mst = Base.Graph(directed = False, weighted = True, traversal = Base.Graph.DFS)
            edges = sorted(self._graph.edges(), key=methodcaller('weight'))
            for edge in edges:
                if self._find(edge.node1()) is not self._find(edge.node2()):
                    self._union(edge.node1(), edge.node2())
                    mst.add(edge.node1(), edge.node2(), edge.weight())
            return mst

    #class for SSSP, uses Dijkstras algorithm
    class SSSP:
        def __init__(self, graph):
            if not graph.directed() or not graph.weighted():
                raise Base.GraphException('SSSP works only for directed, weighted graphs')
            self._graph = graph

        def execute(self, source):
            #Dijkstra
            dist = dict()
            prev = dict()
            Q = list()

            for node in self._graph.nodes():
                dist[node] = math.inf
                prev[node] = None
                Q.append(node)

            dist[source] = 0

            while len(Q) != 0:
                node = min(Q, key=dist.get)
                Q.remove(node)

                for neighbour in self._graph.getNeighbourhood(node):
                    wEdge = self._graph.edge(node, neighbour)
                    alt = dist[node] + wEdge.weight()
                    if alt < dist[neighbour]:
                        dist[neighbour] = alt
                        prev[neighbour] = node

            #Create graph from dist and prev
            G = Base.Graph(directed = True, weighted = True, traversal = Base.Graph.DFS)
            for node, prev in prev.items():
                if prev == None: continue
                wEdge = self._graph.edge(prev, node)
                G.add(wEdge.node1(), wEdge.node2(), wEdge.weight())

            return G


  # 
  # ---------------%<------------------
  # End of my implementation
  #
  
#
# Test suite
#
class Test(unittest.TestCase):
    def test_acceptance(self):
      #
      # Acceptance tests
      #
      self.assertEqual(hasattr(Base,"Graph") and isinstance(Base.Graph, type), True)
      self.assertEqual(hasattr(Base,"Edge") and isinstance(Base.Edge, type), True)
      self.assertEqual(hasattr(Base,"Node") and isinstance(Base.Node, type), True)
      self.assertEqual(hasattr(Base.Graph, "add") and callable(Base.Graph.add), True)
      #
      # Begin of my tests
      # See also https://docs.python.org/3.4/library/unittest.html
      # ---------------%<------------------

    def test_undirected(self):
      G = Base.Graph()
      n1, n2, n3, n4 = Base.Node(), Base.Node(), Base.Node(), Base.Node()
      e1 = G.add(n1, n2)
      e2 = G.add(n1, n2)
      e3 = G.add(n2, n1)
      #check if double edge restriction holds
      self.assertEqual(e1, e2)
      self.assertEqual(e1, e3)
      self.assertEqual(e2, e3)
      #check if double nodes arent possible
      self.assertEqual(G.size(), 2)
      G.add(n3, n2)
      self.assertEqual(G.size(), 3)
      G.add(n3, n4)
      self.assertEqual(G.size(), 4)
      G.add(n4, n1)
      self.assertEqual(G.size(), 4)
      
      #create graph from assignment specification
      G = Base.Graph()
      n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node()
      G.add(n1, n2)
      G.add(n1, n3)
      G.add(n1, n4)
      G.add(n1, n5)
      G.add(n5, n6)
      G.add(n5, n7)
      G.add(n5, n8)
      
      print(G.DOTprint())
      self.assertEqual(G.DOTprint(), "graph g{\nnode[label=\"\"]; \n" \
                       "0 -- 1\n" \
                       "0 -- 2\n" \
                       "0 -- 3\n" \
                       "0 -- 4\n" \
                       "4 -- 5\n" \
                       "4 -- 6\n" \
                       "4 -- 7\n" \
                       "}")
                  
      #test withour pretty printing
      G = Base.Graph(printable = False)
      G.add(n1, n2)
      G.add(n1, n3)
      G.add(n1, n4)
      G.add(n1, n5)
      G.add(n5, n6)
      G.add(n5, n7)
      G.add(n5, n8)
      self.assertEqual(G.size(), 8)
      self.assertEqual(G.numEdges(), 7)
    
    def test_directed(self):
      #test directed graphs 
      G = Base.Graph(directed = True)
      n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
      e1 = G.add(n1, n2)
      e2 = G.add(n1, n2)
      self.assertEqual(e1 is e2, True)
      e3 = G.add(n2, n1)
      self.assertEqual(e2 is e3, False)
      
      G = Base.Graph(directed = True)
      G.add(n1, n2)
      G.add(n2, n3)
      G.add(n2, n4)
      G.add(n2, n5)
      G.add(n6, n5)
      G.add(n5, n7)
      G.add(n5, n8)
      print(G.DOTprint())
      self.assertEqual(G.DOTprint(), "digraph g{\nnode[label=\"\"]; \n" \
               "0 -> 1\n" \
               "1 -> 2\n" \
               "1 -> 3\n" \
               "1 -> 4\n" \
               "5 -> 4\n" \
               "4 -> 6\n" \
               "4 -> 7\n" \
               "}")
    
    def test_neighbourDirected(self):
      #test neighbour representation
      n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
      
      G = Base.Graph(directed = True, representation = Base.Graph.NEIGHBOUR)
      e1 = G.add(n1, n2)
      e2 = G.add(n1, n2)
      self.assertEqual(e1 is e2, True)
      e3 = G.add(n2, n1)
      self.assertEqual(e2 is e3, False)
      del n1, n2
      n1, n2 = Base.Node(), Base.Node()

      G = Base.Graph(directed = True, representation = Base.Graph.NEIGHBOUR)
      G.add(n1, n2)
      G.add(n2, n3)
      G.add(n2, n4)
      G.add(n2, n5)
      G.add(n6, n5)
      G.add(n5, n7)
      G.add(n5, n8)
      print(G.DOTprint())
      self.assertEqual(G.DOTprint(), "digraph g{\nnode[label=\"\"]; \n" \
               "0 -> 1\n" \
               "1 -> 2\n" \
               "1 -> 3\n" \
               "1 -> 4\n" \
               "4 -> 6\n" \
               "4 -> 7\n" \
               "5 -> 4\n" \
               "}")

    def test_neighbourUndirected(self):
      #test DOT printer for undirected neighbour repr  
      n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
          
      G = Base.Graph(directed = False, representation = Base.Graph.NEIGHBOUR)
      nei1 = G.add(n1, n2)
      nei2 = G.add(n1, n2)
      self.assertEqual(nei1 is nei2, True)
      G.add(n2, n3)
      G.add(n2, n4)
      G.add(n2, n5)
      G.add(n6, n5)
      G.add(n5, n7)
      G.add(n5, n8)
      print(G.DOTprint())
      self.assertEqual(G.DOTprint(), "graph g{\nnode[label=\"\"]; \n" \
               "0 -- 1\n" \
               "1 -- 2\n" \
               "1 -- 3\n" \
               "1 -- 4\n" \
               "4 -- 5\n" \
               "4 -- 6\n" \
               "4 -- 7\n" \
               "}")

    def test_weigthed(self):
      #test weights (graphs from assignment)
      n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()

      G = Base.Graph(directed = False, representation = Base.Graph.NEIGHBOUR, weighted = True)
      G.add(n1, n2, 1)
      G.add(n1, n3, 4)
      G.add(n1, n4, 5)
      G.add(n1, n5, 1)
      G.add(n5, n6, 10)
      G.add(n5, n7, 2)
      G.add(n5, n8, 7)
      #check missing and negative weight
      self.assertRaises(Base.GraphException, G.add, n5, n8)
      self.assertRaises(Base.GraphException, G.add, n5, n8, -3)


      print(G.DOTprint())
      self.assertEqual(G.DOTprint(), "graph g{\nnode[label=\"\"]; \n" \
               "0 -- 1 [ label = \"1\" ];\n" \
               "0 -- 2 [ label = \"4\" ];\n" \
               "0 -- 3 [ label = \"5\" ];\n" \
               "0 -- 4 [ label = \"1\" ];\n" \
               "4 -- 5 [ label = \"10\" ];\n" \
               "4 -- 6 [ label = \"2\" ];\n" \
               "4 -- 7 [ label = \"7\" ];\n" \
               "}")
                  
      del G, n1, n2, n3, n4, n5, n6, n7, n8
      n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()

      G = Base.Graph(directed = True, representation = Base.Graph.EDGE, weighted = True)
      G.add(n1, n2, 1)
      G.add(n2, n3, 4)
      G.add(n2, n4, 5)
      G.add(n2, n5, 1)
      G.add(n6, n5, 10)
      G.add(n5, n7, 2)
      G.add(n5, n8, 7)
      print(G.DOTprint())
      self.assertEqual(G.DOTprint(), "digraph g{\nnode[label=\"\"]; \n" \
               "0 -> 1 [ label = \"1\" ];\n" \
               "1 -> 2 [ label = \"4\" ];\n" \
               "1 -> 3 [ label = \"5\" ];\n" \
               "1 -> 4 [ label = \"1\" ];\n" \
               "5 -> 4 [ label = \"10\" ];\n" \
               "4 -> 6 [ label = \"2\" ];\n" \
               "4 -> 7 [ label = \"7\" ];\n" \
               "}")

    def test_unprintable(self):
      #test unprintable graph
      n1, n2 = Base.Node(), Base.Node()
      
      G = Base.Graph(directed = True, representation = Base.Graph.EDGE, weighted = True, printable = False)
      G.add(n1, n2, 4)
      self.assertRaises(Base.GraphException, G.DOTprint)
          
    def test_numEdges(self):
        G = Base.Graph(directed = True, representation = Base.Graph.NEIGHBOUR)
        n1, n2, n3 = Base.Node(), Base.Node(), Base.Node()
        G.add(n1, n2)
        G.add(n2, n1)
        G.add(n2, n3)
        G.add(n1, n3)
        self.assertEqual(G.numEdges(), 4)

        del G
        G = Base.Graph(directed = False, representation = Base.Graph.NEIGHBOUR)
        n3, n4, n5 = Base.Node(), Base.Node(), Base.Node()
        G.add(n3, n4)
        G.add(n4, n5)
        G.add(n3, n5)
        self.assertEqual(G.numEdges(), 3)

    def test_undirectedSearch(self):
        #BFS - edge-rep
        G = Base.Graph(traversal = Base.Graph.BFS)
        n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
        G.add(n1, n2)
        G.add(n2, n3)
        G.add(n3, n4)
        G.add(n5, n6)
        G.add(n6, n7)
        G.add(n7, n8)
        #test wrong params
        self.assertRaises(Base.GraphException, G.search, 1, 'b')
        #test search
        self.assertEqual(G.search(n1, n4), True)
        self.assertEqual(G.search(n5, n8), True)
        self.assertEqual(G.search(n1, n5), False)
        self.assertEqual(G.search(n3, n7), False)

        #DFS - edge-rep
        G.setTraversal(Base.Graph.DFS)
        #test search
        self.assertEqual(G.search(n1, n4), True)
        self.assertEqual(G.search(n5, n8), True)
        self.assertEqual(G.search(n1, n5), False)
        self.assertEqual(G.search(n3, n7), False)

        #BFS - neigh-rep
        G = Base.Graph(traversal = Base.Graph.BFS, representation = Base.Graph.NEIGHBOUR)
        G.add(n1, n2)
        G.add(n2, n3)
        G.add(n3, n4)
        G.add(n5, n6)
        G.add(n6, n7)
        G.add(n7, n8)
        #test search
        self.assertEqual(G.search(n1, n4), True)
        self.assertEqual(G.search(n5, n8), True)
        self.assertEqual(G.search(n1, n5), False)
        self.assertEqual(G.search(n3, n7), False)

        #DFS - neigh-rep
        G.setTraversal(Base.Graph.DFS)
        #test search
        self.assertEqual(G.search(n1, n4), True)
        self.assertEqual(G.search(n5, n8), True)
        self.assertEqual(G.search(n1, n5), False)
        self.assertEqual(G.search(n3, n7), False)

    def test_directedSearch(self):
        #BFS - edge-rep
        G = Base.Graph(directed = True, traversal = Base.Graph.BFS)
        n1, n2, n3, n4, n5, n6, n7, n8, n9 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
        G.add(n1, n2)
        G.add(n1, n3)
        G.add(n2, n4)
        G.add(n4, n5)
        G.add(n4, n6)
        G.add(n4, n7)
        G.add(n7, n3)
        G.add(n7, n8)
        G.add(n9, n9)

        #test search
        self.assertEqual(G.search(n1, n4), True)
        self.assertEqual(G.search(n3, n1), False)
        self.assertEqual(G.search(n4, n8), True)
        self.assertEqual(G.search(n1, n8), True)
        self.assertEqual(G.search(n1, n9), False)
        self.assertEqual(G.search(n9, n9), True)

        #DFS - edge-rep
        G.setTraversal(Base.Graph.DFS)
        #test search
        self.assertEqual(G.search(n1, n4), True)
        self.assertEqual(G.search(n3, n1), False)
        self.assertEqual(G.search(n4, n8), True)
        self.assertEqual(G.search(n1, n8), True)
        self.assertEqual(G.search(n1, n9), False)
        self.assertEqual(G.search(n9, n9), True)

        #BFS - neigh-rep
        G = Base.Graph(directed = True, traversal = Base.Graph.BFS, representation = Base.Graph.NEIGHBOUR)
        n1, n2, n3, n4, n5, n6, n7, n8, n9 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
        G.add(n1, n2)
        G.add(n1, n3)
        G.add(n4, n5)
        G.add(n2, n4)
        G.add(n4, n6)
        G.add(n4, n7)
        G.add(n7, n8)
        G.add(n9, n9)
        
        #test search
        self.assertEqual(G.search(n1, n4), True)
        self.assertEqual(G.search(n3, n1), False)
        self.assertEqual(G.search(n4, n8), True)
        self.assertEqual(G.search(n1, n8), True)
        self.assertEqual(G.search(n1, n9), False)
        self.assertEqual(G.search(n9, n9), True)

        #DFS - neigh-rep
        G.setTraversal(Base.Graph.DFS)
        #test search
        self.assertEqual(G.search(n1, n4), True)
        self.assertEqual(G.search(n3, n1), False)
        self.assertEqual(G.search(n4, n8), True)
        self.assertEqual(G.search(n1, n8), True)
        self.assertEqual(G.search(n1, n9), False)
        self.assertEqual(G.search(n9, n9), True)

    def test_sorted(self):
        n = Base.Node()
        l = [ Base.WeightedEdge(n, n, 3), Base.WeightedEdge(n, n, 2), Base.WeightedEdge(n, n, 5)] 
        l2 = sorted(l, key=methodcaller('weight'))
        for e in l2:
            print(str(e.weight()))

    def test_edgesNeighbourRep(self):
        G = Base.Graph(weighted = True, representation = Base.Graph.NEIGHBOUR)
        n1, n2, n3, n4, n5 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
        G.add(n1, n2, 3)
        G.add(n2, n3, 31)
        G.add(n3, n4, 7)
        G.add(n3, n5, 2)
        G.add(n5, n2, 1)
        self.assertEqual(len(G.edges()), 5)

    def test_MST(self):
        with self.assertRaises(Base.GraphException):
            G = Base.Graph(MST = True)
        with self.assertRaises(Base.GraphException):
            G = Base.Graph(MST = True, weighted = True, directed = True)

        #edge-rep
        G = Base.Graph(weighted = True, MST = True)
        n1, n2, n3, n4, n5, n6, n7 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
        G.add(n1, n2, 7)
        G.add(n1, n4, 5)
        G.add(n2, n3, 8)
        G.add(n2, n4, 9)
        G.add(n2, n5, 7)
        G.add(n3, n5, 5)
        G.add(n4, n5, 15)
        G.add(n4, n6, 6)
        G.add(n5, n6, 8)
        G.add(n5, n7, 9)
        G.add(n6, n7, 11)

        MST = G.MST()

        self.assertEqual(MST.numEdges(), 6)
        self.assertEqual(MST.weighted(), True)
        self.assertEqual(MST.directed(), False)
        #do edges add up to minimum weight?
        sum = 0
        for edge in MST.edges():
            sum += edge.weight() 
        self.assertEqual(sum, 39)
        #is it connected?
        MST.setTraversal(Base.Graph.DFS)
        #pick any startNode
        startNode = MST.nodes()[0]
        for node in MST.nodes():  
            #can we reach all nodes from this node?
            if node is startNode: continue
            self.assertEqual(MST.search(startNode, node), True)

        #neighbour-rep
        G = Base.Graph(weighted = True, MST = True, representation = Base.Graph.NEIGHBOUR)
        G.add(n1, n2, 7)
        G.add(n1, n4, 5)
        G.add(n2, n3, 8)
        G.add(n2, n4, 9)
        G.add(n2, n5, 7)
        G.add(n3, n5, 5)
        G.add(n4, n5, 15)
        G.add(n4, n6, 6)
        G.add(n5, n6, 8)
        G.add(n5, n7, 9)
        G.add(n6, n7, 11)

        MST = G.MST()
        self.assertEqual(MST.numEdges(), 6)
        self.assertEqual(MST.weighted(), True)
        self.assertEqual(MST.directed(), False)
        #do edges add up to minimum weight?
        sum = 0
        for edge in MST.edges():
            sum += edge.weight() 
        self.assertEqual(sum, 39)
        #is it connected?
        MST.setTraversal(Base.Graph.DFS)
        #pick any startNode
        startNode = MST.nodes()[0]
        for node in MST.nodes():  
            #can we reach all nodes from this node?
            if node is startNode: continue
            self.assertEqual(MST.search(startNode, node), True)

    def test_SSSP(self):
        with self.assertRaises(Base.GraphException):
            G = Base.Graph(SSSP = True)
        with self.assertRaises(Base.GraphException):
            G = Base.Graph(SSSP = True, weighted = True, directed = False)

        self._SSSP(Base.Graph.EDGE)
        self._SSSP(Base.Graph.NEIGHBOUR)

    def _SSSP(self, repr):
        G = Base.Graph(weighted = True, SSSP = True, directed = True, representation = repr)
        n0, n1, n2, n3, n4, n5, n6 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
        
        G.add(n0, n1, 5)
        G.add(n1, n0, 1)
        G.add(n0, n2, 20)
        G.add(n0, n3, 3)
        G.add(n2, n4, 6)
        G.add(n2, n3, 15)
        G.add(n3, n4, 1)
        G.add(n4, n5, 3)
        G.add(n4, n6, 12)
        G.add(n5, n6, 3)

        SSSP = G.SSSP(n0)
        self.assertEqual(len(SSSP.nodes()), 7)
        self.assertEqual(SSSP.numEdges(), 6)
        self.assertEqual(SSSP.weighted(), True)
        self.assertEqual(SSSP.directed(), True)
        #do edges add up to correct weight?
        sum = 0
        for edge in SSSP.edges():
            sum += edge.weight() 
        self.assertEqual(sum, 35)
        #is it connected?
        SSSP.setTraversal(Base.Graph.DFS)
        startNode = n0
        for node in SSSP.nodes():  
            #can we reach all nodes from this node?
            if node is startNode: continue
            self.assertEqual(SSSP.search(startNode, node), True)

        #check other startnode
        SSSP = G.SSSP(n3)
        self.assertEqual(len(SSSP.nodes()), 4)
        self.assertEqual(SSSP.numEdges(), 3)
        self.assertEqual(SSSP.weighted(), True)
        self.assertEqual(SSSP.directed(), True)
        #do edges add up to correct weight?
        sum = 0
        for edge in SSSP.edges():
            sum += edge.weight() 
        self.assertEqual(sum, 7)
        #is it connected?
        SSSP.setTraversal(Base.Graph.DFS)
        startNode = n3
        for node in SSSP.nodes():  
            #can we reach all nodes from this node?
            if node is startNode: continue
            self.assertEqual(SSSP.search(startNode, node), True)

      # ---------------%<------------------
      # End of my tests
      #    
if __name__ == '__main__':
    unittest.main()

