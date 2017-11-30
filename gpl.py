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

    class Graph():
        # "Constants"
        NEIGHBOUR = "neighbour"
        EDGE = "edge"
        BFS = "bfs"
        DFS = "dfs"

        def __init__(self, directed = False, representation = None, weighted = False, printable = True, traversal = None):
            #Edge representation is the default
            if (representation == None) or (representation != Base.Graph.NEIGHBOUR):
                self._representation = Base.Graph.EDGE
                self._edges = []
            else:
                self._representation = representation
            #default is undirected 
            if directed == True:
                self._directed = True
            else:
                self._directed = False
            #default is unweighted
            if weighted == True:
                self._weighted = True
            else:
                self._weighted = False
            #default is printable
            if printable == False:
                self._printable = False
                self.DOTprint = None
            else:
                self._printable = True
            #default is not traversable
            if traversal == Base.Graph.BFS:
                self._traversal = Base.Graph.BFS
            elif traversal == Base.Graph.DFS:
                self._traversal = Base.Graph.DFS
            else:
                self._traversal = None
            self._nodes = []                    
        
        def nodeID(self, node):
            return self._nodes.index(node)
        
        def edges(self):
            if self._representation == Base.Graph.EDGE:
                return self._edges
            else:
                return None
            
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
                    elif edge.node2 is node:
                        neighbourhood.append(edge.node1())

            elif self._representation == Base.Graph.NEIGHBOUR:
                for neighbour in node.neighbours():
                    neighbourhood.append(neighbour.opposite())
            else:
                raise Base.GraphException('Unknown edge representation!')
            return neighbourhood
            
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
      self.assertEqual(callable(getattr(G, "DOTprint", None)), False)

    def test_wrongParams(self):
      #test wrong parameters
      G = Base.Graph(directed = "a", representation = 37, weighted = 2, printable = "b")
      self.assertEqual(G.representation(), Base.Graph.EDGE)
      self.assertEqual(G.directed(), False)
      self.assertEqual(G.weighted(), False)
      self.assertEqual(G.printable(), True)
      G = Base.Graph(representation = Base.Graph.NEIGHBOUR)
      with self.assertRaises(TypeError):
          G.add(2, "3")

          
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
        G.add(n2, n4)
        G.add(n4, n5)
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

      # ---------------%<------------------
      # End of my tests
      #    
if __name__ == '__main__':
    unittest.main()
