import random
class Node():
        def __init__(self, pos, number):
            self.pos = pos
            self.number = number

        def get_pos(self):
            return self.pos

        def get_number(self):
            return self.number  
class Hamiltonian():
    def __init__(self, X, Y):
        self.X=X
        self.Y=Y
        self.HALF_X=X//2
        self.HALF_Y=Y//2

    def create_nodes(self):
        nodes = [[Node((x * 2 + 1, y * 2 + 1), x + y * self.HALF_X) for y in range(0, self.HALF_Y)] for x in range(0, self.HALF_X)]
        return nodes
    def create_edges(self):
        edges = [[0 for y in range(0, self.HALF_Y * self.HALF_X)] for x in range(0, self.HALF_X * self.HALF_Y)]

        skiplist = [self.HALF_X * x for x in range(0, self.HALF_X)]
        for x in range(0, self.HALF_X * self.HALF_Y):
            for y in range(0, self.HALF_Y * self.HALF_X):
                if not (x == y):
                    if (x + 1 == y and y not in skiplist): edges[x][y] = random.randint(1, 3)
                    elif (x + self.HALF_X == y): edges[x][y] = random.randint(1, 3)

        return edges
    def hamiltonian_cycle(self,nodes, edges):
        points = []
        for edge in edges:
            for pos_x in range(0, self.HALF_X):
                for pos_y in range(0, self.HALF_Y):
                    if (nodes[pos_x][pos_y].get_number() == edge[0][0]):
                        start = nodes[pos_x][pos_y].get_pos()
                    if (nodes[pos_x][pos_y].get_number() == edge[0][1]):
                        end = nodes[pos_x][pos_y].get_pos()
            points.append(start)
            points.append(((start[0]+end[0])//2, (start[1]+end[1])//2))
            points.append(end)

        cycle = [(0, 0)]

        curr = cycle[0]
        dir = (1, 0)

        while len(cycle) < self.X * self.Y:
            x = curr[0]
            y = curr[1]

            if dir == (1, 0): #right
                if ((x + dir[0], y + dir[1] + 1) in points and (x + 1, y) not in points):
                    curr = (x + dir[0], y + dir[1])
                else:
                    if ((x, y + 1) in points and (x + 1, y + 1) not in points):
                        dir = (0, 1)
                    else:
                        dir = (0, -1)
            
            elif dir == (0, 1): #down
                if ((x + dir[0], y + dir[1]) in points and (x + dir[0] + 1, y + dir[1]) not in points):
                    curr = (x + dir[0], y + dir[1])
                else:
                    if ((x, y + 1) in points and (x + 1, y + 1) in points):
                        dir = (1, 0)
                    else:
                        dir = (-1, 0)

            elif dir == (-1, 0): #left
                if ((x, y) in points and (x, y+1) not in points):
                    curr = (x + dir[0], y + dir[1])
                else:
                    if ((x, y + 1) not in points):
                        dir = (0, -1)
                    else:
                        dir = (0, 1)

            elif dir == (0, -1): #up
                if ((x, y) not in points and (x + 1, y) in points):
                    curr = (x + dir[0], y + dir[1])
                else:
                    if ((x + 1, y) in points):
                        dir = (-1, 0)
                    else:
                        dir = (1, 0)

            if curr not in cycle:
                cycle.append(curr)
        cycle.append((0,0))

        return points, cycle
        
    def prims_algoritm(self,edges):
        clean_edges = []
        for x in range(0, self.HALF_X * self.HALF_Y):
            for y in range(0, self.HALF_Y * self.HALF_X):
                if not (edges[x][y] == 0):
                    clean_edges.append(((x, y), edges[x][y]))
                
        visited = []
        unvisited = [x for x in range(self.HALF_X * self.HALF_Y)]
        curr = 0

        final_edges = []
        while len(unvisited) > 0:
            visited.append(curr)

            for number in unvisited:
                if number in visited:
                    unvisited.remove(number)

            my_edges = []
            for edge in clean_edges:
                if ((edge[0][0] in visited or edge[0][1] in visited) and not (edge[0][0] in visited and edge[0][1] in visited)):
                    my_edges.append(edge)

            min_edge = ((-1, -1), 999)

            for edge in my_edges:
                if (edge[1] < min_edge[1]):
                    min_edge = edge
            
            if len(unvisited) == 0:
                break

            final_edges.append(min_edge)

            if min_edge[0][0] == -1:
                curr = unvisited[0]
            else:
                if (min_edge[0][1] in visited):
                    curr = min_edge[0][0]
                else:
                    curr = min_edge[0][1]

        return final_edges