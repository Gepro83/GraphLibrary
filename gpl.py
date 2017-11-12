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
      def __init__(self, opposite, weight = None):
          self._opposite = opposite
          self._weight = weight
          
      def opposite(self):
          return self._opposite
      def weight(self):
          return self._weight
      
  class Edge:
      def __init__(self, node1, node2, weight = None):
          self._node1 = node1
          self._node2 = node2
          self._weight = weight
          
      def node1(self):
          return self._node1
      def node2(self):
          return self._node2
      def weight(self):
          return self._weight

  class Graph():
        # "Constants"
      NEIGHBOUR = "neighbour"
      EDGE = "edge"
      DEFAULT_WEIGHT = 0
      
      def __init__(self, directed = False, representation = None, weighted = False):
          if representation == None:
              representation = Base.Graph.EDGE
          self._directed = directed
          self._representation = representation
          self._weighted = weighted
          self._nodes = {}
          self._nodeCoutner = 0
          if self._representation == Base.Graph.EDGE:  
                self._edges = []
      
      def nodeID(self, node):
          return self._nodes.get(node)
      
      def edges(self):
          if self._representation == Base.Graph.EDGE:
              return self._edges
          else:
              return None
      
      #add an edge
      #in digraphs the direction is from newNode1 to newNode2
      #if no weight is given in a weighted graph DEFAULT_WEIGHT is used as a default value
      #only non-negative weights are allowed, negative weights will be corrected to the default
      def add(self, newNode1, newNode2, weight = None):
          if self._weighted == True:
              if weight == None:
                  weight = Base.Graph.DEFAULT_WEIGHT
              if weight < 0:
                  weight = Base.Graph.DEFAULT_WEIGHT
          
          #use different method for neighbour representation
          if self._representation == Base.Graph.NEIGHBOUR:
                    return self._neighbourAdd(newNode1, newNode2, weight)
          # check if edge already exists
          for edge in self._edges:
              if edge.node1() is newNode1 and edge.node2() is newNode2:
                  return edge
              if not self._directed:
                  if edge.node1() is newNode2 and edge.node2() is newNode1:
                      return edge
              
          #add the new edge
          e = Base.Edge(newNode1, newNode2, weight)
          self._edges.append(e)              
          #add nodes
          self._addNode(newNode1)
          self._addNode(newNode2)
          return e
      
      #"private" method for adding edges in neighbour representation
      def _neighbourAdd(self, newNode1, newNode2, weight):
          #check if edge already exists
          for node in self._nodes.keys():
              if node is newNode1:
                  for neighbour in node.neighbours():
                      if neighbour.opposite() is newNode2:
                          return neighbour
          
          #add nodes
          self._addNode(newNode1)
          self._addNode(newNode2)
          #add neighbours    
          node1neighbour = Base.Neighbour(newNode2, weight)
          newNode1.addNeighbour(node1neighbour)
          if not self._directed: 
              node2neighbour = Base.Neighbour(newNode1, weight)
              newNode2.addNeighbour(node2neighbour)
              
          return node1neighbour
      
      def _addNode(self, node):
          #only add nodes that do not exist in the graph yet
          if node not in self._nodes:
              self._nodes[node] = self._nodeCoutner
              self._nodeCoutner += 1
      
      def size(self):
          return len(self._nodes)
      
      def numEdges(self):
          if self._representation == Base.Graph.EDGE:
              return len(self._edges)
          else:
              return None
  
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
              if self._directed:
                  DOTstring += self._singleDOTedge(edge.node1(), edge.node2(), edge.weight())
              else:
                  DOTstring += self._singleDOTedge(edge.node1(), edge.node2(), edge.weight())
          return DOTstring
      
      #returns a string containing dot syntax of the edges in neighbour representation
      def _DOTneighbour(self):
          DOTstring = ""
          visited = []
          for node in self._nodes.keys():
              if self._directed:
                  for neighbour in node.neighbours():
                      DOTstring += self._singleDOTedge(
                              node, neighbour.opposite(), neighbour.weight())
                      
              else:
                  for neighbour in node.neighbours():
                      if neighbour.opposite() in visited:
                          continue
                      DOTstring += self._singleDOTedge(
                              node, neighbour.opposite(), neighbour.weight())

              visited.append(node)
              
          return DOTstring
      
      #returns the correct DOT representation for the current graph of a single edge
      #followed by a linebreak
      #a value for weight is expected for weighted graphs
      def _singleDOTedge(self, node1, node2, weight = None):
          edgeString = ""
          if self._directed:
              edgeString = (str(self.nodeID(node1)) + " -> " + 
                            str(self.nodeID(node2)))
          else:
              edgeString = (str(self.nodeID(node1)) + " -- " + 
                            str(self.nodeID(node2)))
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
      #test DOT printer for undirected neighbour repr  
      del G, n1, n2, n3, n4, n5, n6, n7, n8
      n1, n2, n3, n4, n5, n6, n7, n8 = Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node(), Base.Node()
          
      G = Base.Graph(directed = False, representation = Base.Graph.NEIGHBOUR)
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

      G = Base.Graph(directed = False, representation = Base.Graph.NEIGHBOUR, weighted = True)
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
      # ---------------%<------------------
      # End of my tests
      #    
if __name__ == '__main__':
    unittest.main()
