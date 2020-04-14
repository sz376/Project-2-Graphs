import random
import sys
import math
import heapq

class GridNode:
  def __init__(self, x, y, nodeVal):
    self.val = nodeVal
    self.coordinates = (x,y)
    self.visited = False
    self.nodes = []    #does this contain neighbors?

  def __lt__(self, other):
    in1=self.val
    in2=other.val
    if in1 < in2:
      return in1
    return in2

class GridGraph:
  def __init__(self):
    self.allNodes = []
    self.nodeMap = {}

  def getNode(self, val):
    return self.nodeMap.get(val)

  def getAllNodes(self):
    return self.nodeMap

  def addGridNode(self, x, y, nodeVal):
    node = GridNode(x, y, nodeVal)
    self.allNodes.append(node)            #works fine with your other functions but consider checking for dup nodes.
    self.nodeMap[nodeVal] = node

  def isNeighbor(first, second):
    firstX = first.coordinates[0]
    firstY = first.coordinates[1]
    secondX = second.coordinates[0]
    secondY = second.coordinates[1]

    if (firstX + 1 == secondX and firstY == secondY) or (firstX == secondX and firstY + 1 == secondY) or (firstX-1 == secondX and firstY == secondY) or (firstX == secondX and firstY - 1 == secondY):
      return True
    return False

  def addUndirectedEdge(self, first, second):
    if first == None or second == None:
      return
    count = 0
    firstIdx = -1
    secondIdx = -1
    for node in self.allNodes:
      if firstIdx != -1 and secondIdx != -1: # 
        break
      if node.val == first.val:
        firstIdx = count
      if node.val == second.val:
        secondIdx = count
      count += 1

    if firstIdx == secondIdx:
      return
    else:
      self.allNodes[firstIdx].nodes.append(second) # consider checking for duplicates either here or in addGridNode to be through
      self.allNodes[secondIdx].nodes.append(first)
    
  def removeUndirectedEdge(self, first, second):
    if first == None or second == None:
      return
    count = 0
    firstIdx = -1
    secondIdx = -1
    for node in self.allNodes:                   #since this block of code was used in addedge as well, consider making it a seperate funct. for clarity
      if firstIdx != -1 and secondIdx != -1:     #for example: a function that returns int tuple
        break
      if node.val == first.val:
        firstIdx = count
      if node.val == second.val:
        secondIdx = count
      count += 1
    
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

    if idx1 == -1 or idx2 == -1:
      return
    
    self.allNodes[firstIdx].nodes.pop(idx2)
    self.allNodes[secondIdx].nodes.pop(idx1)
    
    # missing a getAllNodes funct.
    
def createRandomGridGraph(n):
  g = GridGraph()
  numNodes = 0

  for x in range(n):
    for y in range(n):
      g.addGridNode(x, y, numNodes)
      numNodes += 1

  for node in g.allNodes:
    if node.val + n < n*n:
      #decide if we should add an edge between the node above
      #making it an 90% chance because we want to make sure there's a connection to the end
      if random.randint(0,9) < 9:
        g.addUndirectedEdge(node, g.getNode(node.val+n))
    if node.val % n != n - 1 and node.val + 1 < n*n:
      #decide if we should add an edge between the node to the right
      if random.randint(0,9) < 9:
        g.addUndirectedEdge(node, g.getNode(node.val+1))
  
  return g

def minDist(distances, visited):
  ans = None
  m = math.inf
  for curr in distances.keys():
    if visited[curr] != True and distances[curr] <= m:
      m = distances[curr]
      ans = curr
  return ans

def heuristic(start, end):
  #manhattan distance
  xdiff = end.coordinates[0] - start.coordinates[0]
  ydiff = end.coordinates[1] - start.coordinates[1]
  return abs(xdiff) + abs(ydiff) 

def astarHeap(sourceNode, destNode):  
  if not sourceNode or not destNode:
    return []

  mapDistances = {}
  mapVisited = {}
  mapParents = {}
  mapHeuristicDistances = {}
  min_dist = []
  
  mapDistances[sourceNode] = 0
  mapParents[sourceNode] = None
  mapHeuristicDistances[sourceNode] = heuristic(sourceNode, destNode)

  mapVisited[destNode] = False
  mapVisited[sourceNode] = False
  heapq.heappush(min_dist, (mapHeuristicDistances[sourceNode], sourceNode))
  while min_dist:
    # “Finalize” curr.
    currDistance, curr = heapq.heappop(min_dist)
    if mapVisited[curr] == True:
      continue
    mapVisited[curr] = True
    if mapVisited[destNode] == True:
      break
    # Iterate over its neighbors, “relax” each neighbor:
    for neighbor in curr.nodes:
      if neighbor not in mapDistances:
        mapDistances[neighbor] = math.inf
        mapVisited[neighbor] = False
        mapParents[neighbor] = None

      if mapVisited[neighbor] != True:
        if mapDistances[curr] + 1 < mapDistances[neighbor]:
          mapParents[neighbor] = curr
          mapDistances[neighbor] = mapDistances[curr] + 1
          mapHeuristicDistances[neighbor] = mapDistances[neighbor] + heuristic(neighbor, destNode)
          heapq.heappush(min_dist, (mapHeuristicDistances[neighbor], neighbor))
  
  path = []
  if curr != destNode:
    return path
  path.insert(0, curr.val)
  while mapParents[curr] != None:
    path.insert(0, mapParents[curr].val)
    curr = mapParents[curr]
  return path

def astar(sourceNode, destNode):   #consider removing this if its not used
  if not sourceNode or not destNode:
    return []
  # Create an empty map of nodes to distances. Initialize every node to map to infinity.
  mapDistances = {}
  mapVisited = {}
  mapParents = {}
  mapHeuristicDistances = {}
    
  # Set the distance for the sourceNode to 0. Let curr be the sourceNode. Calculate heuristic
  mapDistances[sourceNode] = 0
  mapParents[sourceNode] = None
  mapHeuristicDistances[sourceNode] = heuristic(sourceNode, destNode)
  curr = sourceNode
  mapVisited[destNode] = False
  # While curr is not null and its distance is not infinity.
  while curr != None and curr != destNode:
    # “Finalize” curr.
    mapVisited[curr] = True
    # Iterate over its neighbors, “relax” each neighbor:
    for neighbor in curr.nodes:
      if neighbor not in mapDistances:
        mapDistances[neighbor] = math.inf
        mapVisited[neighbor] = False
        mapParents[neighbor] = None
      # For each neighbor that is not finalized, update its distance (if less than its current distance) to the sum of curr’s distance and the weight of the edge between curr and this neighbor.
      if mapVisited[neighbor] != True:
        if mapDistances[curr] < mapDistances[neighbor]:
          mapParents[neighbor] = curr
          mapDistances[neighbor] = mapDistances[curr]
          mapHeuristicDistances[neighbor] = mapDistances[neighbor] + heuristic(neighbor, destNode)
      # Set curr to the next min distance node – the node with the smallest distance that is not yet finalized.
    curr = minDist(mapHeuristicDistances, mapVisited)
  
  path = []
  if curr != destNode:
    return path
  path.insert(0,curr.val)
  while mapParents[curr] != None:
    path.insert(0,mapParents[curr].val)
    curr = mapParents[curr]
  return path

g = createRandomGridGraph(10000)

nodes = g.getAllNodes()
for node in nodes.values():
  print(node.val)
  for edge in node.nodes:
    print("edge", edge.val)

path = astarHeap(g.getNode(0),g.getNode(9999))
print(path)

print()
#edgextra credit !!!!!!
print("Number of Nodes finalized: ", len(path))
