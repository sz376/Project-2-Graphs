import random
import sys
import math
import heapq

class Node:
  def __init__(self, val):
    self.val = val
    self.visited = False
    self.nodes = []

  def __lt__(self, other):
    in1=self.val
    in2=other.val
    if in1 < in2:
      return in1
    return in2

class Edge:
  def __init__(self, dest, weight):
    self.dest = dest
    self.weight = weight

class WeightedGraph:
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
  
  def addWeightedEdge(self, first, second, weight):
    if first == None or second == None:
      return
    if first == second:
      return
    try:
      self.nodeMap[first.val].nodes.append(Edge(second, weight))
    except ValueError:
      return

  def removeDirectedEdge(self, first, second):
    if first == None or second == None:
      return
    idx2 = -1
    count = 0
    for edge in self.allNodes[self.allNodes.index(first)].nodes:
      if edge.dest.val == second.val:
        idx2 = count
        break
      count += 1
    if idx2 == -1:
      return
    try:
      self.allNodes[self.allNodes.index(first)].nodes.pop(idx2)
    except ValueError:
      return

def createRandomCompleteWeightedGraph(n):
  g = WeightedGraph()

  for i in range(n):
    g.addNode(i)
  #adds n-1 edges to every node
  results = [g.addWeightedEdge(g.getNode(i), g.getNode(j), random.randint(1,10)) for i in range(n) for j in range(n)]

  return g

def createLinkedList(n):
  g = WeightedGraph()
  prev = None
  for i in range(n):
    g.addNode(i)
    curr = g.allNodes[-1]
    if prev:
      g.addWeightedEdge(prev, curr, 1)
    prev = curr
  return g

def minDist(distances, visited):
  ans = None
  m = math.inf
  for curr in distances.keys():
    if visited[curr] != True and distances[curr] <= m:
      m = distances[curr]
      ans = curr
  return ans

def dijkstras(start):
  
  mapDistances = {}
  mapVisited = {}
  mapParents = {}
  minDist = []

  mapDistances[start] = 0
  mapVisited[start] = False
  mapParents[start] = None
  heapq.heappush(minDist, (mapDistances[start], start))
  
  while minDist:
    currDistance, curr = heapq.heappop(minDist)
    if mapVisited[curr] == True:
      continue
    # “Finalize” curr.
    mapVisited[curr] = True
    # Iterate over its neighbors, “relax” each neighbor:
    for neighbor in curr.nodes:
      if neighbor.dest not in mapDistances:
        mapDistances[neighbor.dest] = math.inf
        mapVisited[neighbor.dest] = False
        mapParents[neighbor.dest] = None
      if mapVisited[neighbor.dest] != True:
        if currDistance + neighbor.weight < mapDistances[neighbor.dest]:
          mapParents[neighbor.dest] = curr
          mapDistances[neighbor.dest] = currDistance + neighbor.weight
          heapq.heappush(minDist, (currDistance + neighbor.weight, neighbor.dest))

  return mapDistances

def dijkstrasExtraCredit(start, end):
  
  mapDistances = {}
  mapVisited = {}
  mapParents = {}
  minDist = []

  mapDistances[start] = 0
  mapVisited[start] = False
  mapParents[start] = None
  heapq.heappush(minDist, (mapDistances[start], start))
  
  while minDist:
    currDistance, curr = heapq.heappop(minDist)
    if mapVisited[curr] == True:
      continue
    # “Finalize” curr.
    mapVisited[curr] = True
    if curr == end:
      count = 0
      for node in mapVisited:
        if mapVisited[node] == True:
          count += 1
      return count
    # Iterate over its neighbors, “relax” each neighbor:
    for neighbor in curr.nodes:
      if neighbor.dest not in mapDistances:
        mapDistances[neighbor.dest] = math.inf
        mapVisited[neighbor.dest] = False
        mapParents[neighbor.dest] = None
      if mapVisited[neighbor.dest] != True:
        if currDistance + neighbor.weight < mapDistances[neighbor.dest]:
          mapParents[neighbor.dest] = curr
          mapDistances[neighbor.dest] = currDistance + neighbor.weight
          heapq.heappush(minDist, (currDistance + neighbor.weight, neighbor.dest))

  return len(mapDistances)

'''
EDGEXTRA CREDIT!!!
Note: 10000 will not work on a typical computer or it will take an insane amount of time since there are 99,990,000 edges. I had to run it using the OSL computers on AFS which have more computing power/space, so for the sake of not breaking your computer, I just have it set to 100. It works with 10000 on AFS if you want to see for yourself :)
'''
x = 100
g = createRandomCompleteWeightedGraph(x)

print()
print("RUNNING DIJKSTRAS")
nodesFinalized = dijkstrasExtraCredit(g.getNode(0), g.getNode(99))

print()
#edgextra credit !!!!!!
print("Number of Nodes finalized: ", nodesFinalized, "out of", x)

print()
g = createRandomCompleteWeightedGraph(10)
nodes = g.getAllNodes()
for node in nodes.values():
  print(node.val)
  for edge in node.nodes:
    print("edge", edge.dest.val, "weight", edge.weight)

print()
print("RUNNING DIJKSTRAS")
distances = dijkstras(g.getNode(0))

for key in distances.keys():
  nodeval = key.val
  print("node", nodeval, "distance", distances[key])

print()


print()
print("Linked List")

g = createLinkedList(4)
nodes = g.getAllNodes()
for node in nodes.values():
  print(node.val)
  for edge in node.nodes:
    print("edge", edge.dest.val, "weight", edge.weight)

print()
print("RUNNING DIJKSTRAS")
distances = dijkstras(g.getNode(0))

for key in distances.keys():
  nodeval = key.val
  print("node", nodeval, "distance", distances[key])