from http.client import FOUND, NOT_FOUND
import math
import os
from platform import java_ver
from re import T
import sys


def getCostMove(student_nod1, student_nod2):
        if abs(student_nod1.i - student_nod2.i) == 1:
            return 1
        else:
            if student_nod1.j < student_nod2.j and student_nod1.j % 2 == 0:
                return 0
            elif student_nod1.j < student_nod2.j and student_nod1.j % 2 == 1:
                return 2
            
            if student_nod2.j < student_nod1.j and student_nod2.j % 2 == 0:
                return 0
            else:
                return 2

def getDirection(student_nod1, student_nod2):
    move_cost = getCostMove(student_nod1, student_nod2)
    
    if student_nod1.j < student_nod2.j:
        if move_cost == 0:
            return '>'
        elif move_cost == 2:
            return '>>'
    elif student_nod1.j > student_nod2.j:
        if move_cost ==0:
            return '<'
        elif move_cost == 1:
            return '<<'

    else:
        if student_nod1.i < student_nod2.i:
            return 'v'
    
    return '^'

class Nod:
    def __init__(self, name, heuristic = 1):
        self.name = name
        self.heuristic = heuristic

        if heuristic == 0:
            self.euristicaBanala()
        elif heuristic == 1:
            self.euristica1()
        elif heuristic == 2:
            self.euristica2()
        else:
            self.euristicaInadmisibila()

        self.setPosition()

    def setPosition(self):
        for i in range(len(classroom_config)):
                for j in range(len(classroom_config[i])):
                    if classroom_config[i][j] == self.name:
                        self.i = i
                        self.j = j

    def isAffectedByListening(self):
        listened_student = ascultati[0]

        listened_student_nod = Nod(listened_student[0])

        if abs(self.i - listened_student_nod.i) < 2:
            if abs(self.j - listened_student_nod.j) <= 3:
                return True

        return False 


    #TODO euristici
    def euristicaBanala(self):
        if self.name == final_node:
            self.h = 0
        else:
            #search for the positin of the student_node
            for i in range(len(classroom_config)):
                for j in range(len(classroom_config[i])):
                    if classroom_config[i][j] == self.name:
                        i_student_node = i
                        j_student_node = j
                    elif classroom_config[i][j] == final_node:
                        i_student_scope = i
                        j_student_scope = j


            self.h = abs(i_student_node - i_student_scope) + abs(j_student_node - j_student_scope)

    def euristica1(self):
        #if the student is the scope student
        if self.name == final_node:
            self.h = 0 

        else:
            distance = 0
        #search for the positin of the student_node
            for i in range(len(classroom_config)):
                for j in range(len(classroom_config[i])):
                    if classroom_config[i][j] == self.name:
                        i_student_node = i
                        j_student_node = j
                    elif classroom_config[i][j] == final_node:
                        i_student_scope = i
                        j_student_scope = j

            #determine if the scope_student is in the left, right, on the same row
            if j_student_node < 2:
                row_student_node = 1
            elif j_student_node < 4:
                row_student_node =2
            else:
                row_student_node =3
            
            if j_student_scope < 2:
                row_student_scope = 1 
            elif j_student_scope <4:
                row_student_scope = 2
            else:
                row_student_scope = 3

            #case when row_student_node < row_student_scope
            i = i_student_node
            j = j_student_node
            while row_student_node < row_student_scope:
                if i < len(classroom_config) - 2:
                    distance += len(classroom_config) - 2 - i
                    i = len(classroom_config) - 2
                    
                if j  % 2 == 0:
                    j += 1
                row_student_node += 1
                distance += 2
                j += 1
                
            #case when row_student_node > row_student_scope
            while row_student_scope < row_student_node:
                if i < len(classroom_config) - 2:
                    distance += len(classroom_config) - 2 - i
                    i = len(classroom_config) - 2
                
                if j % 2 == 1 :
                    j -= 1

                row_student_node -= 1
                distance += 2
                j -= 1

            #case when students are on the same row
            distance += abs(i - i_student_scope)

            self.h = distance
    
    def euristica2(self):
        #if the student is the scope student
        if self.name == final_node:
            self.h = 0 

        else:
            distance = 0
        #search for the positin of the student_node
            for i in range(len(classroom_config)):
                for j in range(len(classroom_config[i])):
                    if classroom_config[i][j] == self.name:
                        i_student_node = i
                        j_student_node = j
                    elif classroom_config[i][j] == final_node:
                        i_student_scope = i
                        j_student_scope = j

            self.h = (i_student_node - i_student_scope)*(i_student_node - i_student_scope) + (j_student_node - j_student_scope)*(j_student_node - j_student_scope)
            self.h = math.sqrt(self.h)

    def euristicaInadmisibila(self):
        if self.name == final_node:
            self.h = 0 

        else:
            distance = 0
        #search for the positin of the student_node
            for i in range(len(classroom_config)):
                for j in range(len(classroom_config[i])):
                    if classroom_config[i][j] == self.name:
                        i_student_node = i
                        j_student_node = j
                    elif classroom_config[i][j] == final_node:
                        i_student_scope = i
                        j_student_scope = j

    def __repr__(self):
        return f"{self.name},{self.h},i: {self.i},j: {self.j}"


class NodParcurgere:
    def __init__(self,node,parent,expandat,g, direction=''):
        self.node = node
        self.parent = parent
        self.direction = direction
        self.g = g
        self.expandat = expandat
        self.f = self.node.h + self.g

    def expandeaza(self):
        self.expandat = 1
        succesors = []

        i = self.node.i
        j = self.node.j
        name = self.node.name

        #students from first bank
        if i == 0 and j == 0:
            if classroom_config[i][j+1] != 'liber' and [classroom_config[i][j+1], name] not in suparati and [name, classroom_config[i][j+1]] not in suparati:
                succesors.append(classroom_config[i][j+1])
            
            if classroom_config[i+1][j] != 'liber' and [classroom_config[i+1][j], name] not in suparati and [name, classroom_config[i+1][j]] not in suparati:
                succesors.append(classroom_config[i+1][j])

        elif i ==0 and  j == len(classroom_config[i])-1:
            if classroom_config[i][j-1] != 'liber' and [classroom_config[i][j-1], name] not in suparati and [name, classroom_config[i][j-1]] not in suparati:
                succesors.append(classroom_config[i][j-1])
            
            if classroom_config[i+1][j] != 'liber' and [classroom_config[i+1][j], name] not in suparati and [name, classroom_config[i+1][j]] not in suparati:
                succesors.append(classroom_config[i+1][j])

        elif i == 0:
            if classroom_config[i][j-1] != 'liber' and [classroom_config[i][j-1], name] not in suparati and [name, classroom_config[i][j-1]] not in suparati:
                if (j-1) %2 != 1:
                    succesors.append(classroom_config[i][j-1])

            if classroom_config[i][j+1] != 'liber' and [classroom_config[i][j+1], name] not in suparati and [name, classroom_config[i][j+1]] not in suparati:
                if (j+1) %2 != 0:
                    succesors.append(classroom_config[i][j+1])
            
            if classroom_config[i+1][j] != 'liber' and [classroom_config[i+1][j], name] not in suparati and [name, classroom_config[i+1][j]] not in suparati:
                succesors.append(classroom_config[i+1][j])

        #students from last bank
        if i == len(classroom_config)-1 and j == 0:
            if classroom_config[i][j+1] != 'liber' and [classroom_config[i][j+1], name] not in suparati and [name, classroom_config[i][j+1]] not in suparati:
                succesors.append(classroom_config[i][j+1])
            
            if classroom_config[i-1][j] != 'liber' and [classroom_config[i-1][j], name] not in suparati and [name, classroom_config[i-1][j]] not in suparati:
                succesors.append(classroom_config[i-1][j])

        elif i == len(classroom_config)-1 and  j == len(classroom_config[i])-1:
            if classroom_config[i][j-1] != 'liber' and [classroom_config[i][j-1], name] not in suparati and [name, classroom_config[i][j-1]] not in suparati:
                succesors.append(classroom_config[i][j-1])
            
            if classroom_config[i-1][j] != 'liber' and [classroom_config[i-1][j], name] not in suparati and [name, classroom_config[i-1][j]] not in suparati:
                succesors.append(classroom_config[i-1][j])
        
        elif i == len(classroom_config)-1:
            if classroom_config[i][j-1] != 'liber' and [classroom_config[i][j-1], name] not in suparati and [name, classroom_config[i][j-1]] not in suparati:
                succesors.append(classroom_config[i][j-1])

            if classroom_config[i][j+1] != 'liber' and [classroom_config[i][j+1], name] not in suparati and [name, classroom_config[i][j+1]] not in suparati:
                succesors.append(classroom_config[i][j+1])
            
            if classroom_config[i-1][j] != 'liber' and [classroom_config[i-1][j], name] not in suparati and [name, classroom_config[i-1][j]] not in suparati:
                succesors.append(classroom_config[i-1][j])


        #students from the left wall
        if j == 0 and i != 0 and i != len(classroom_config)-1:
            if classroom_config[i][j+1] != 'liber' and [classroom_config[i][j+1], name] not in suparati and [name, classroom_config[i][j+1]] not in suparati:
                succesors.append(classroom_config[i][j+1])
            
            if classroom_config[i-1][j] != 'liber' and [classroom_config[i-1][j], name] not in suparati and [name, classroom_config[i-1][j]] not in suparati:
                succesors.append(classroom_config[i-1][j])

            if classroom_config[i+1][j] != 'liber' and [classroom_config[i+1][j], name] not in suparati and [name, classroom_config[i+1][j]] not in suparati:
                succesors.append(classroom_config[i+1][j])


        #students from the right wall
        if j == len(classroom_config[i])-1 and i != 0 and i != len(classroom_config)-1:
            if classroom_config[i][j-1] != 'liber' and [classroom_config[i][j-1], name] not in suparati and [name, classroom_config[i][j-1]] not in suparati:
                succesors.append(classroom_config[i][j-1])

            if classroom_config[i-1][j] != 'liber' and [classroom_config[i-1][j], name] not in suparati and [name, classroom_config[i-1][j]] not in suparati:
                succesors.append(classroom_config[i-1][j])

            if classroom_config[i+1][j] != 'liber' and [classroom_config[i+1][j], name] not in suparati and [name, classroom_config[i+1][j]] not in suparati:
                succesors.append(classroom_config[i+1][j])

        #students who don't stay at any margin
        if i != 0 and i != len(classroom_config)-1 and j != 0 and j != len(classroom_config[i])-1:
            if classroom_config[i][j-1] != 'liber' and [classroom_config[i][j-1], name] not in suparati and [name, classroom_config[i][j-1]] not in suparati:
                if i == len(classroom_config) - 2 or (j-1) % 2 != 1:
                    succesors.append(classroom_config[i][j-1])

            if classroom_config[i][j+1] != 'liber' and [classroom_config[i][j+1], name] not in suparati and [name, classroom_config[i][j+1]] not in suparati:
                if i == len(classroom_config) - 2 or (j+1) % 2 != 0:
                    succesors.append(classroom_config[i][j+1])

            if classroom_config[i-1][j] != 'liber' and [classroom_config[i-1][j], name] not in suparati and [name, classroom_config[i-1][j]] not in suparati:
                succesors.append(classroom_config[i-1][j])

            if classroom_config[i+1][j] != 'liber' and [classroom_config[i+1][j], name] not in suparati and [name, classroom_config[i+1][j]] not in suparati:
                succesors.append(classroom_config[i+1][j])

        succesors_nod = []
        
        for s in succesors:
            s_nod = Nod(s)
            if s_nod.isAffectedByListening() == False:
                succesors_nod.append(s_nod)

        return succesors_nod

    def test_scop(self):
        #TODO implement recursive path from the first node to the final
        #TODO not hard coding path
        if self.node.name == final_node:
            return True
                    
class Problema:
    def __init__(self):
        self.open = []
        self.close = []
        self.solutions = []
        self.paths = []

    def listenStudent(self, moves):
        while self.listen_list != [] and moves > 0:
            self.listen_list[0][1] -= 1
            if self.listen_list[0][0] == 0:
                self.listen_list.pop(0)
            moves -= 1

    def getPath(self, student):
        path = []
        while student.parent != -1:
            aux = []
            aux.append(student.node.name)
            aux.append(student.direction)
            path.append(aux)
            student = student.parent

        #adding the first student    
        aux = []
        aux.append(student.node.name)
        aux.append(student.direction)
        path.append(aux)
        
        return path

    def simulationBFS(self):
        np_start = NodParcurgere(start_student, -1, 0, 0)
        self.open.append(np_start)
        cnt = 0 
        self.listen_list = ascultati

        while self.open != [] and cnt < 10000:
            cnt += 1
            nod_curent = self.open[0]
            self.listenStudent(nod_curent.g)
            
            succesors = nod_curent.expandeaza()
            self.open.pop(0)
            #self.close.append(nod_curent)
            print(succesors)

            if nod_curent.test_scop() == True:
                print("Nod scop")
                path = self.getPath(nod_curent)

                path = path[::-1]
                #for i in range(len(path)):
                #   print(path[i][1],path[i][0],sep=" ")

                self.paths.append(path)
            
            for student in succesors:
                g = getCostMove(nod_curent.node, student)
                direction = getDirection(nod_curent.node, student)
                
                #verify if the student is already in close list
                ok = 0
                path = self.getPath(nod_curent)

                for node in path:
                    if node[0] ==  student.name:
                        ok = 1
                
                #if student was not visited yet(is not in close)
                if ok == 0:
                    self.open.append(NodParcurgere(student, nod_curent,0,g, direction))

            
    def simulationDFS(self):
        np_start = NodParcurgere(start_student, -1, 0, 0)
        cnt = 0
        
        #visited_dict is a dictionary use to mark the succesors visited for each node
        visited_dict = {}
        for row in classroom_config:
            for student in row:
                visited_dict[student] = []


        self.open.append(np_start)
        self.listen_list = ascultati

        while self.open != [] and cnt<1000:
            cnt += 1
            nod_curent = self.open[len(self.open) - 1]
            self.listenStudent(nod_curent.g)

            print('Nodul curent este: ', nod_curent.node)
            succesors = nod_curent.expandeaza()
            self.open.pop()

            if nod_curent.test_scop() == True:
                print('Nod scop')

                path = self.getPath(nod_curent)

                path = path[::-1]

                self.paths.append(path)

            print(succesors)
            for student in succesors:
                g = getCostMove(nod_curent.node, student)
                direction = getDirection(nod_curent.node, student)

                ok = 0
                #verify if the succesor is not in stack(open list)
                #or succesors was not treated by the current node until now
                if student.name in visited_dict[nod_curent.node.name]:
                    ok = 1
                
                #for open_node in self.open:
                #    if open_node.node.name == student.name:
                #        ok = 1
                
                if ok == 0:
                    # mark succesor as visited
                    visited_dict[nod_curent.node.name].append(student.name)
                    visited_dict[student.name].append(nod_curent.node.name)
                    self.open.append(NodParcurgere(student, nod_curent, 0, g, direction))
            
            print(visited_dict)
            for node in self.open:
                print(node.node.name, end= " ")
            print('\n')

    def simulationIDF(self, max_depth):
        np_start = NodParcurgere(start_student, -1, 0 , 0)
        for i in range(max_depth):
            found, remaining = self.DLS(np_start, i)
            if found != 'null':
                path = self.getPath(found)
                path = path[::-1]
                self.paths.append(path)

                #return found

            elif not remaining:
                return 'null'

    def DLS(self, nod_curent, depth):
        if depth == 0:
            if nod_curent.test_scop() == True:
                return (nod_curent, True)
            else:
                return ('null', True)

        elif depth > 0:
            any_remaining = False
            succesors = nod_curent.expandeaza()
            
            for successor in succesors:
                g = getCostMove(nod_curent.node, successor)
                direction = getDirection(nod_curent.node, successor)
                found, remaining = self.DLS(NodParcurgere(successor, nod_curent, 0, g, direction), depth - 1)

                if found != 'null':
                    return (found, True)
                if remaining:
                    any_remaining = True

            return ('null', any_remaining)

    def simulationAStar(self, ways):
        no_solutions = 0
        np_start = NodParcurgere(start_student, -1, 0, 0)
        self.open.append(np_start)
        cnt = 0 
        self.listen_list = ascultati

        while self.open != [] and cnt < 10000:
            cnt += 1
            self.open.sort(key = lambda elem : (elem.f, -elem.g))
            nod_curent = self.open[0]
            self.listenStudent(nod_curent.g)
            
            succesors = nod_curent.expandeaza()
            self.open.pop(0)
            #self.close.append(nod_curent)
            print(succesors)

            if nod_curent.test_scop() == True:
                print("Nod scop")
                no_solutions += 1

                path = self.getPath(nod_curent)

                path = path[::-1]
                #for i in range(len(path)):
                #   print(path[i][1],path[i][0],sep=" ")

                self.paths.append(path)

                if no_solutions == ways:
                    return True
            
            for student in succesors:
                g = getCostMove(nod_curent.node, student)
                direction = getDirection(nod_curent.node, student)
                
                #verify if the student is already in close list
                ok = 0
                path = self.getPath(nod_curent)

                for node in path:
                    if node[0] ==  student.name:
                        ok = 1
                
                #if student was not visited yet(is not in close)
                if ok == 0:
                    g_final = nod_curent.g + g
                    self.open.append(NodParcurgere(student, nod_curent,0, g_final, direction))

    def simulationAStarOptimised(self):
        np_start = NodParcurgere(start_student, -1, 0, 0)
        self.open.append(np_start)
        cnt = 0
        self.listen_list = ascultati
        
        while self.open != [] and cnt <10000:
            self.open.sort(key = lambda elem : (elem.f, -elem.g))
            nod_curent = self.open[0]
            self.listenStudent(nod_curent.g)


            self.open.pop(0)
            self.close.append(nod_curent)

            if nod_curent.test_scop() == True:
                path = self.getPath(nod_curent)
                path = path[::-1]
                self.paths.append(path)
                return True
            
            succesors = nod_curent.expandeaza()

            for student in succesors:
                nod_nou = None
                ok = 0

                path = self.getPath(nod_curent)
                for nod_drum in path:
                    if nod_drum[0] == student.name:
                        ok = 1
                        break
                
                if ok == 0:
                    yes_open = 0
                    yes_close = 0
                    g = getCostMove(nod_curent.node, student)
                    direction = getDirection(nod_curent.node, student)
                    
                    for open_node in self.open:
                        if open_node.node.name == student.name:
                            if nod_curent.g + g  + student.h < open_node.f:
                                yes_open = 1
                                self.open.remove(open_node)
                                g_final = nod_curent.g + g
                                nod_nou = NodParcurgere(student, nod_curent, 0, g_final, direction)

                    for close_node in self.close:
                        if close_node.node.name == student.name:
                            if nod_curent.g + g + student.h < close_node.f:
                                yes_close = 1
                                self.close.remove(close_node)
                                g_final = nod_curent.g + g
                                nod_nou = NodParcurgere(student, nod_curent, 0 , g_final, direction)

                    if nod_nou != None:
                        self.open.append(nod_nou)
                    elif yes_open == 0 and yes_close == 0:
                        g_final = nod_curent.g + g
                        nod_nou = NodParcurgere(student, nod_curent, 0 , g_final, direction)
                        self.open.append(nod_nou)
        return False

    def simulateIDAStar(self):
        np_start = NodParcurgere(start_student, -1,0, 0)
        bound = np_start.node.h
        path = [np_start]

        while True:
            t = self.search(path, 0, bound)
            if t == 'found':
                return (path, bound)
            if t == float('inf'):
                return 'not found'

            bound = T
    
    def search(self, path, g, bound):
        nod_curent = path[len(path) - 1]
        f = g + nod_curent.node.h

        if f > bound:
            return f
        if nod_curent.test_scop() == True:
            return 'found'

        min = float('inf')

        succesors = nod_curent.expandeaza()

        for succesor in succesors:
            if succesor not in path:
                g_move = getCostMove(nod_curent.node, succesor)
                direction = getDirection(nod_curent.node, succesor)

                path.append(NodParcurgere(succesor, nod_curent, 0, g + g_move, direction))
                t = self.search(path, g + g_move, bound)
                if t == 'found':
                    return 'found'
                if t < min:
                    min = t 
                path.pop()
        
        return min

def readData(file):
    f = open(file, 'r')
    
    cnt = 0
    suparati = []
    classroom_config = []
    ascultati = []
    start_node = ""
    final_node = ""
    for line in f.readlines():
        if cnt == 0 and line != 'suparati\n':
            aux = []
            line = line.split()
            for student in line:
                aux.append(student)
            #g1.write(aux)    
            classroom_config.append(aux)

        elif line == 'suparati\n':
            cnt += 1
        
        elif cnt == 1 and line != 'ascultati\n':
            aux1 = []
            line = line.split()
            aux1.append(line[0])
            aux1.append(line[1])
            suparati.append(aux1)

        elif line == 'ascultati\n':
            cnt += 1

        elif cnt == 2 and line != 'mesaj\n':
            aux = []
            line = line.split()
            aux.append(line[0])
            aux.append(int(line[1]))
            ascultati.append(aux)

        elif line == 'mesaj\n':
            cnt += 1
        
        elif cnt == 3:
            line = line.split()
            start_node = line[0]
            final_node = line[1]
    print(cnt)
    return classroom_config, suparati, ascultati, start_node, final_node    
if __name__=="__main__":
    #inputFolder = sys.argv[1]
    #outputFolder = sys.argv[2]
    #noSolutions = int(sys.argv[3])
    #timeout = int(sys.argv[4])

    global classroom_config

    global suparati

    global ascultati

    global start_node

    global final_node  
    g1 = open("/home/bogdan/Downloads/Tema1/f1.txt", 'w')
    '''
    for file in os.listdir(inputFolder):
        fileName = inputFolder + '/' + file
        g1.write(fileName)
        classroom_config, suparati, ascultati, start_node, final_node = readData(fileName)
    '''
    classroom_config, suparati, ascultati, start_node, final_node = readData("/home/bogdan/Downloads/Tema1/input/exemplu.txt")
    print(suparati)


    #testing zone

    
    g2 = open("/home/bogdan/Downloads/Tema1/f2.txt", 'w')
    g3 = open("/home/bogdan/Downloads/Tema1/f3.txt", 'w')
    global start_student
    start_student = Nod(start_node)
    nodParcurgere = NodParcurgere(start_student,-1,0,0)
    print(nodParcurgere.expandeaza())
    print(start_student.isAffectedByListening())

    bfs = Problema()
    bfs.simulationBFS()
    print(len(bfs.paths))

    for i in range(len(bfs.paths)):
        g1.write('Path number: %d' % i)
        for j in range(len(bfs.paths[i])):
            g1.write(bfs.paths[i][j][1] + ' ' +  bfs.paths[i][j][0])
        g1.write('\n')
    '''
    dfs = Problema()
    print(dfs.open)
    dfs.simulationDFS()
    print(len(dfs.paths))

    for i in range(len(dfs.paths)):
        print('Path number: %d' % i)
        for j in range(len(dfs.paths[i])):
            print(dfs.paths[i][j][1], dfs.paths[i][j][0], end = ' ')
        print('\n')

    print('A*')
    aStarOptimised = Problema()
    aStarOptimised.simulationAStarOptimised()
    for i in range(len(aStarOptimised.paths)):
        print('Path number: %d' % i)
        for j in range(len(aStarOptimised.paths[i])):
            print(aStarOptimised.paths[i][j][1], aStarOptimised.paths[i][j][0], end = ' ')
        print('\n')

    print('A* neoptimizat')
    aStar  = Problema()
    aStar.simulationAStar(5)
    for i in range(len(aStar.paths)):
        g2.write('Path number: %d' % i)
        for j in range(len(aStar.paths[i])):
            g2.write(aStar.paths[i][j][1] + ' ' + aStar.paths[i][j][0])
        g2.write('\n')


    print('dfi')
    dfi = Problema()
    dfi.simulationIDF(15)
    for i in range(len(dfi.paths)):
        g3.write('Path number: %d' % i)
        for j in range(len(dfi.paths[i])):
            g3.write(dfi.paths[i][j][1] + ' ' + dfi.paths[i][j][0])
        g3.write('\n')

    print('ida*')
    idaStar = Problema()
    print(idaStar.simulateIDAStar())
    '''
    #TODO wait feature in case that the ticket can't be passed



