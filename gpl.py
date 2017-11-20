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

class Base():
  #
  # Begin of my implementation
  # ---------------%<------------------
          # "Constants"
  NEIGHBOUR = "neighbour"
  EDGE = "edge"
  DEFAULT_WEIGHT = 0
  
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
      def __init__(self, opposite, weight = None):
          super().__init__(opposite)
          if weight == None:
              self._weight = Base.DEFAULT_WEIGHT
          else:
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
      def __init__(self, node1, node2, weight = None):
          super().__init__(node1, node2)
          if weight == None:
              self._weight = Base.DEFAULT_WEIGHT
          else:
              self._weight = weight
          
      def weight(self):
          return self._weight
          
  class Graph():
      
      def __init__(self, directed = False, representation = None, weighted = False, printable = True):
          #Edge representation is the default
          if (representation == None) or (representation != Base.NEIGHBOUR):
              self._representation = Base.EDGE
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
          else:
              self._printable = True
          self._nodes = []
                
      
      def nodeID(self, node):
          return self._nodes.index(node)
      
      def edges(self):
          if self._representation == Base.EDGE:
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
      
      #add an edge
      #in digraphs the direction is from m to n
      #if no weight is given in a weighted graph DEFAULT_WEIGHT is used as a default value
      #only non-negative weights are allowed, negative weights will be corrected to the default
      def add(self, m, n, weight = None):
          if self._weighted == True:
              if weight == None:
                  weight = Base.DEFAULT_WEIGHT
              if weight < 0:
                  weight = Base.DEFAULT_WEIGHT
          
          #use different method for neighbour representation
          if self._representation == Base.NEIGHBOUR:
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
          if self._representation == Base.EDGE:
              return len(self._edges)
          else:
              return None
  
      #DOT pretty printer
      def DOTprint(self):
          if not self._printable:
              return ""
          #start a graph
          if self._directed:
              DOTstring = 'digraph g{\nnode[label=""]; \n'
          else:
              DOTstring = 'graph g{\nnode[label=""]; \n'
         
          if self._representation == Base.EDGE:
              DOTstring += self._DOTedges()
          elif self._representation == Base.NEIGHBOUR:
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

    def test_my(self):
      #
      # Begin of my tests
      # See also https://docs.python.org/3.4/library/unittest.html
      # ---------------%<------------------
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
      
      #test directed graphs 
      G = Base.Graph(directed = True)
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
                  
      #test neighbour representation
      del G, n1, n2, n3, n4, n5, n6, n7, n8
      n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
      
      G = Base.Graph(directed = True, representation = Base.NEIGHBOUR)
      e1 = G.add(n1, n2)
      e2 = G.add(n1, n2)
      self.assertEqual(e1 is e2, True)
      e3 = G.add(n2, n1)
      self.assertEqual(e2 is e3, False)
      del n1, n2
      n1, n2 = Base.Node(), Base.Node()

      G = Base.Graph(directed = True, representation = Base.NEIGHBOUR)
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
      #test DOT printer for undirected neighbour repr  
      del G, n1, n2, n3, n4, n5, n6, n7, n8
      n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
          
      G = Base.Graph(directed = False, representation = Base.NEIGHBOUR)
      G.add(n1, n2)
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
      #test weights (graphs from assignment)
      del G, n1, n2, n3, n4, n5, n6, n7, n8
      n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()

      G = Base.Graph(directed = False, representation = Base.NEIGHBOUR, weighted = True)
      G.add(n1, n2, 1)
      G.add(n1, n3, 4)
      G.add(n1, n4, 5)
      G.add(n1, n5, 1)
      G.add(n5, n6, 10)
      G.add(n5, n7, 2)
      G.add(n5, n8, 7)
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

      G = Base.Graph(directed = True, representation = Base.EDGE, weighted = True)
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
                  
      #test unprintable graph
      del G, n1, n2
      n1, n2 = Base.Node(), Base.Node()
      
      G = Base.Graph(directed = True, representation = Base.EDGE, weighted = True, printable = False)
      G.add(n1, n2, 4)
      self.assertEqual(G.DOTprint(), "")
      
      #test wrong parameters
      G = Base.Graph(directed = "a", representation = 37, weighted = 2, printable = "b")
      self.assertEqual(G.representation(), Base.EDGE)
      self.assertEqual(G.directed(), False)
      self.assertEqual(G.weighted(), False)
      self.assertEqual(G.printable(), True)
      G = Base.Graph(representation = Base.NEIGHBOUR)
      with self.assertRaises(TypeError):
          G.add(2, "3")
      # ---------------%<------------------
      # End of my tests
      #    
if __name__ == '__main__':
    unittest.main()
