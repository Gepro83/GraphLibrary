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

class Base:
  #
  # Begin of my implementation
  # ---------------%<------------------
  #
  
  class Node:
      pass
          
  class Edge:
      def __init__(self, node1, node2):
          self._node1 = node1
          self._node2 = node2
          
      def node1(self):
          return self._node1
      def node2(self):
          return self._node2

  class Graph:
      def __init__(self):
          self._nodes = {}
          self.nodeCoutner = 0
          self._edges = []
      
      def nodes(self):
          return self._nodes
      
      def edges(self):
          return self._edges
      
      def add(self, newNode1, newNode2):
          # check if edge already exists
          for edge in self._edges:
              if edge.node1() is newNode1 and edge.node2() is newNode2:
                  return edge
              elif edge.node1() is newNode2 and edge.node2() is newNode1:
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
      
      def size(self):
          return len(self._nodes)
      
      def numEdges(self):
          return len(self._edges)
  
  #DOT pretty printer
  def DOTprint(self, graph):
      #start a graph
      DOTstring = 'graph g{\nnode[label=""]; \n'
      #add every edge
      for edge in graph.edges():
          DOTstring += str(graph.nodes()[edge.node1()]) + " -- " + str(graph.nodes()[edge.node2()]) + "\n"
      #finish graph
      DOTstring += "}"
      print(DOTstring)
      
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
      
      #test pretty printer
      B = Base()
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
      B.DOTprint(G)
      pass
  
      # ---------------%<------------------
      # End of my tests
      #    

if __name__ == '__main__':
    unittest.main()
