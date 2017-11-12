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
      def __init__(self, opposite):
          self._opposite = opposite
          
      def opposite(self):
          return self._opposite
      
  class Edge:
      def __init__(self, node1, node2):
          self._node1 = node1
          self._node2 = node2
          
      def node1(self):
          return self._node1
      def node2(self):
          return self._node2

  class Graph():
        # "Constants"
      NEIGHBOUR = "neighbour"
      EDGE = "edge"
      
      def __init__(self, directed = False, representation = None):
          if representation == None:
              representation = Base.Graph.EDGE
          self._directed = directed
          self._representation = representation
          self._nodes = {}
          self.nodeCoutner = 0
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
      def add(self, newNode1, newNode2):
          #use different method for neighbour representation
          if self._representation == Base.Graph.NEIGHBOUR:
                    return self._add(newNode1, newNode2)
          # check if edge already exists
          for edge in self._edges:
              if edge.node1() is newNode1 and edge.node2() is newNode2:
                  return edge
              if not self._directed:
                  if edge.node1() is newNode2 and edge.node2() is newNode1:
                      return edge
              
          #add the new edge
          e = Base.Edge(newNode1, newNode2)
          self._edges.append(e)              
          #only add nodes that do not exist in the graph yet
          if newNode1 not in self._nodes:
              self._nodes[newNode1] = self.nodeCoutner
              self.nodeCoutner += 1
          if newNode2 not in self._nodes:
              self._nodes[newNode2] = self.nodeCoutner
              self.nodeCoutner += 1
          return e
      
      #"private" method for adding edges in neighbour representation
      def _add(self, newNode1, newNode2):
          #check if edge already exists
          for node in self._nodes.keys():
              if node is newNode1:
                  for neighbour in node.neighbours():
                      if neighbour.opposite() is newNode2:
                          return neighbour
          
          if newNode1 in self._nodes.keys():
              neighbour = Base.Neighbour(newNode2)
              newNode1.addNeighbour(neighbour)
              
              
              
              
          return
      
      def size(self):
          return len(self._nodes)
      
      def numEdges(self):
          return len(self._edges)
  
      #DOT pretty printer
      def DOTprint(self):
          #start a graph
          if self._directed:
              DOTstring = 'digraph g{\nnode[label=""]; \n'
          else:
              DOTstring = 'graph g{\nnode[label=""]; \n'
          #add every edge
          for edge in self._edges:
              if self._directed:
                  DOTstring += (str(self._nodes.get(edge.node1())) + " -> " + 
                                str(self._nodes.get(edge.node2())) + "\n")
              else:
                  DOTstring += (str(self._nodes.get(edge.node1())) + " -- " + 
                                str(self._nodes.get(edge.node2())) + "\n")
          #finish graph
          DOTstring += "}"
          return DOTstring
          
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
      # ---------------%<------------------
      # End of my tests
      #    
if __name__ == '__main__':
    unittest.main()
