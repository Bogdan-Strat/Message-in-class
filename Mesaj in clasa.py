from platform import java_ver


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
    def __init__(self,name):
        self.name = name
        self.euristicaBanala()
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


if __name__=="__main__":
    global classroom_config
    classroom_config = [['ionel', 'alina', 'teo', 'eliza', 'carmen', 'monica'],
                          ['george', 'diana', 'bob', 'liber', 'nadia', 'mihai'],
                          ['liber', 'costin', 'anda', 'bogdan', 'dora', 'marin'],
                          ['luiza', 'simona', 'dana', 'cristian', 'tamara', 'dragos'],
                          ['mihnea', 'razvan', 'radu', 'patricia', 'gigel', 'elena'],
                          ['liber', 'andrei' , 'oana', 'victor', 'liber', 'dorel'],
                          ['viorel', 'alex', 'ela', 'nicoleta', 'maria', 'gabi']]

    global suparati
    suparati = [['ionel', 'george'],
                ['teo', 'eliza'],
                ['teo', 'luiza'],
                ['oana', 'victor'],
                ['ela', 'nicoleta'],
                ['dragos','alina'],
                ['dragos', 'elena']]

    global ascultati 
    ascultati = [['monica', 4],
                 ['maria', 1]]

    global start_node
    start_node = 'ionel'

    global final_node  
    final_node = 'dragos'

    #testing zone
    start_student = Nod(start_node)
    nodParcurgere = NodParcurgere(start_student,-1,0,0)
    print(nodParcurgere.expandeaza())
    print(start_student.isAffectedByListening())

    bfs = Problema()
    bfs.simulationBFS()
    print(len(bfs.paths))

    for i in range(len(bfs.paths)):
        print('Path number: %d' % i)
        for j in range(len(bfs.paths[i])):
            print(bfs.paths[i][j][1], bfs.paths[i][j][0], end = ' ')
        print('\n')

    dfs = Problema()
    print(dfs.open)
    dfs.simulationDFS()
    print(len(dfs.paths))

    for i in range(len(dfs.paths)):
        print('Path number: %d' % i)
        for j in range(len(dfs.paths[i])):
            print(dfs.paths[i][j][1], dfs.paths[i][j][0], end = ' ')
        print('\n')





