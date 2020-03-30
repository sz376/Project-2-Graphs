import random
import sys

class Node:
  def __init__(self, val):
    self.val = val
    self.visited = False
    self.nodes = []

class Graph:
  def __init__(self):
    self.allNodes = []

  def getNode(self, val):
    for node in self.allNodes:
      if node.val == val:
        return node
    return None

  def addNode(self, nodeVal):
    node = Node(nodeVal)
    self.allNodes.append(node)

  def addUndirectedEdge(self, first, second):
    count = 0
    firstIdx = -1
    secondIdx = -1
    for node in self.allNodes:
      if firstIdx != -1 and secondIdx != -1:
        break
      if node.val == first.val:
        firstIdx = count
      if node.val == second.val:
        secondIdx = count
      count += 1

    if firstIdx == -1 or secondIdx == -1:
      return
  
    if firstIdx == secondIdx:
      #edge with itself, no need to add twice
      self.allNodes[firstIdx].nodes.append(second)
    else:
      self.allNodes[firstIdx].nodes.append(second)
      self.allNodes[secondIdx].nodes.append(first)

  def removeUndirectedEdge(self, first, second):
    count = 0
    firstIdx = -1
    secondIdx = -1
    for node in self.allNodes:
      if firstIdx != -1 and secondIdx != -1:
        break
      if node.val == first.val:
        firstIdx = count
      if node.val == second.val:
        secondIdx = count
      count += 1

    if firstIdx == -1 or secondIdx == -1:
      return
    
    idx1 = -1
    idx2 = -1
    count = 0
    for node in self.allNodes[firstIdx].nodes:
      if node.val == second.val:
        idx2 = count
        break
      count += 1
    count = 0
    for node in self.allNodes[secondIdx].nodes:
      if node.val == first.val:
        idx1 = count
        break
      count += 1

    self.allNodes[firstIdx].nodes.pop(idx2)
    self.allNodes[secondIdx].nodes.pop(idx1)

  def getAllNodes(self):
    d = {}
    for node in self.allNodes:
      d[node] = node
    return d

def createRandomUnweightedGraph(n):
  g = Graph()
  if n == 0:
    return g

  edges = []
  for i in range(n):
    g.addNode(i)
     # decide how many edges each node will have
    if n == 1:
      return g
    if n == 2:
      edges.append(random.randint(0,1))
    else:
      edges.append(random.randint(0,n//2))
  # decide for each edge, which nodes it will be between
  pairs = []
  for i in range(n):
    for num in range(edges[i]):
      found = True
      while found:
        node2 = random.randint(0,n-1)
        pair = (i, node2)
        reverse = (node2, i)
        if pair in pairs or reverse in pairs:
          found = True
        else:
          found = False
      pairs.append((i, node2))

  for pair in pairs:
    first = None
    second = None
    
    for node in g.getAllNodes():
      if first and second:
        break
      if node.val == pair[0]:
        first = node
      if node.val == pair[1]:
        second = node

    g.addUndirectedEdge(first,second)

  return g

def createLinkedList(n):
  g = Graph()
  prev = None
  for i in range(n):
    g.addNode(i)
    curr = g.allNodes[-1]
    if prev:
      g.addUndirectedEdge(prev, curr)
    prev = curr
  return g
  
def BFTIterLinkedList(graph):
  return GraphSearch.BFTIter(graph)

def BFTRecLinkedList(graph):
  return GraphSearch.BFTRec(graph)

class GraphSearch:
  def DFSIter(start, end):
    path = []
    s = []
    if start and end:
      if start.visited != True:
        start.visited = True
        s.append(start)
        while len(s) > 0:
          curr = s.pop()
          path.append(curr)
          if curr.val == end.val:
            return path
          for vertex in curr.nodes:
            if vertex.visited != True:
              vertex.visited = True
              s.append(vertex)
    return None

  def DFSRec(start, end):
    if start and end:
      return GraphSearch.myDFSRec(start, end)
    return None

  def myDFSRec(start, end, path = []):
    path.append(start)
    start.visited == True
    if start.val == end.val:
      return path
    for vertex in start.nodes:
      if vertex not in path:
        newPath = GraphSearch.myDFSRec(vertex, end, path)
        if newPath:
          return newPath
    return None
  
  def BFTRec(graph):
    path = []
    queue = []
    nodesInGraph = graph.getAllNodes()
    for node in nodesInGraph:
      if node.visited == False:
        node.visited = True
        queue.append(node)
        GraphSearch.myBFTRec(graph, queue, path)
    return path

  def myBFTRec(graph, queue, path):
    if len(queue) == 0:
      return
    curr = queue.pop(0)
    path.append(curr)
    for vertex in curr.nodes:
      if vertex.visited == False:
        vertex.visited = True
        queue.append(vertex)
    GraphSearch.myBFTRec(graph, queue, path)

  def BFTIter(graph):
    path = []
    q = []
    nodesInGraph = graph.getAllNodes()
    for node in nodesInGraph:
      if node.visited != True:
        node.visited = True
        q.append(node)
        while len(q) > 0:
          curr = q.pop(0)
          path.append(curr)
          for vertex in curr.nodes:
            if nodesInGraph[vertex].visited != True:
              nodesInGraph[vertex].visited = True
              q.append(vertex)
    return path

g = createRandomUnweightedGraph(8)

nodes = g.getAllNodes()
for node in nodes:
  print(node.val)
  for node in node.nodes:
    print("edge", node.val)

path = GraphSearch.DFSIter(g.getNode(0), g.getNode(3))
print("dfs")
if path:
  for node in path:
    print(node.val)
else:
  print("no valid dfs iter")

nodes2 = g.getAllNodes()
for node1 in nodes2:
  node1.visited = False

path = GraphSearch.BFTIter(g)
print("bft")
for node in path:
  print(node.val)

nodes2 = g.getAllNodes()
for node1 in nodes2:
  node1.visited = False

path = GraphSearch.DFSRec(g.getNode(0), g.getNode(3))
print("DFS Rec")
if path:
  for node in path:
    print(node.val)
else:
  print("no valid dfs rec")

nodes2 = g.getAllNodes()
for node1 in nodes2:
  node1.visited = False

path = GraphSearch.BFTRec(g)
print("BFT Rec")
if path:
  for node in path:
    print(node.val)
else:
  print("no valid bft rec") 

print()

newGraph = createLinkedList(10)
print("Recursion Limit: ", sys.getrecursionlimit())

llNodes = newGraph.getAllNodes()
for node in llNodes:
  print(node.val)
  for node in node.nodes:
    print("edge", node.val)

print()
returnedPath = BFTIterLinkedList(newGraph)
print("BFT Iter LL")
for node in returnedPath:
  print(node.val, end= " ")

print()
print()

nodes2 = newGraph.getAllNodes()
for node1 in nodes2:
  node1.visited = False

returnedPath = BFTRecLinkedList(newGraph)
print("BFT Rec LL")
for node in returnedPath:
  print(node.val, end= " ")

print()