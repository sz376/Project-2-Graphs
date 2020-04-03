import random
import sys
import math

class Node:
  def __init__(self, val):
    self.val = val
    self.visited = False
    self.nodes = []

class DirectedGraph:
  def __init__(self):
    self.allNodes = []
    self.nodeMap = {}

  def getNode(self, val):
    return self.nodeMap.get(val)

  def addNode(self, nodeVal):
    node = Node(nodeVal)
    self.allNodes.append(node)
    self.nodeMap[nodeVal] = node
  
  def getAllNodes(self):
    return self.nodeMap

  def addDirectedEdge(self, first, second):
    if first == None or second == None:
      return
    else:
      try:
        if second not in self.allNodes[self.allNodes.index(first)].nodes:
          self.allNodes[self.allNodes.index(first)].nodes.append(second)
      except ValueError:
        return

  def removeUndirectedEdge(self, first, second):
    if first == None or second == None:
      return

    idx2 = -1
    count = 0
    for node in self.allNodes[self.allNodes.index(first)].nodes:
      if node.val == second.val:
        idx2 = count
        break
      count += 1
    if idx2 == -1:
      return
    try:
      self.allNodes[self.allNodes.index(first)].nodes.pop(idx2)
    except ValueError:
      return

def createRandomDAGIter(n):
  g = DirectedGraph()
  lenRow = math.floor(math.sqrt(n))
  
  for i in range(n):
    g.addNode(i)

  for node in g.allNodes:
    if node.val + lenRow < n:
      #decide if we should add an edge between the node above
      if random.randint(0,2) < 2:
        g.addDirectedEdge(node, g.getNode(node.val+lenRow))
    if node.val % lenRow != lenRow - 1 and node.val + 1 < n:
      #decide if we should add an edge between the node to the right
      if random.randint(0,2) < 2:
        g.addDirectedEdge(node, g.getNode(node.val+1))

  return g

class TopSort:
  def Kahns(graph):
    inDegree = TopSort.initializeInDegreeMap(g)
    topSort = []
    queueInDegree0 = TopSort.addNodesWithoutDependenciesToQueue(inDegree, [])

    while len(queueInDegree0) > 0:
      currNode = queueInDegree0[0]
      topSort.append(currNode)

      for node in g.allNodes:
        if node == currNode:
          for neighbor in node.nodes:
            inDegree[neighbor] -= 1
            if inDegree[neighbor] == 0:
              queueInDegree0.append(neighbor)
          queueInDegree0.pop(0)
          break

    return topSort

  def initializeInDegreeMap(g):
    inDegree = {}
    for node in g.allNodes:
      inDegree[node] = 0

    for node in g.allNodes:
      for neighbor in node.nodes:
        inDegree[neighbor] += 1
    
    return inDegree

  def addNodesWithoutDependenciesToQueue(inDegree, queue):
    for node in inDegree:
      if inDegree[node] == 0:
        queue.append(node)
        inDegree[node] = -1
    return queue

  def mDFS(graph):
    stack = []
    numNodes = len(g.allNodes)
    for vertex in g.allNodes:
      if vertex.visited != True:
        TopSort.mDFSHelper(vertex, stack)
    output = []
    while stack:
      output.append(stack.pop())
    
    return output
  
  def mDFSHelper(node, stack):
    node.visited = True
    for neighbor in node.nodes:
      if neighbor.visited != True:
        TopSort.mDFSHelper(neighbor, stack) 
    stack.append(node)
  
g = createRandomDAGIter(1000)

nodes = g.getAllNodes()
for val, node in nodes.items():
  print(val)
  for neighbor in node.nodes:
    print("edge", neighbor.val)

out = TopSort.mDFS(g)
print("mDFS")
for node in out:
  print(node.val)

for node in g.getAllNodes().values():
  node.visited = False

out = TopSort.Kahns(g)
print("Kahns")
for node in out:
  print(node.val)
