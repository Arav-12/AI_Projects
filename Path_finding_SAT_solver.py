#!/usr/bin/env python3
from Agent import * # See the Agent.py file
from pysat.solvers import Glucose3
#### All your code can go here.
#!/usr/bin/env python3
#### All your code can go here.
#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.
#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.

knowledge_base = Glucose3()
literals={}
safe_to_travel=[]
safe_explored=[]
parent_node={}


def main():
  
    global knowledge_base
    global literals
    global safe_to_travel
    global safe_explored
    global parent_node
    literal_count=1
    for i in range(4): #Mines from 1 to 16
        for j in range(4):
            literals["M"+str(i+1)+str(j+1)]=literal_count
            literal_count+=1
    for i in range(4): # percept=0 17 to 32
        for j in range(4):
            literals["=0"+str(i+1)+str(j+1)]=literal_count
            literal_count+=1
    for i in range(4): #percept=1 fromm 33 to 48
        for j in range(4):
            literals["=1"+str(i+1)+str(j+1)]=literal_count
            literal_count+=1
    for i in range(4): #percept>1 fromm 49 to 64
        for j in range(4):
            literals[">1"+str(i+1)+str(j+1)]=literal_count
            literal_count+=1
    '''
    Above each number from 1->64 denotes a literal that will be used in our knowledge_base

    '''
    
    knowledge_base.add_clause([-literals["M"+str(1)+str(1)]]) #Initial Clause that gaurantees that there will be no mine in [1,1]
    knowledge_base.add_clause([-literals["M"+str(4)+str(4)]]) ##Initial Clause that gaurantees that there will be no mine in [4,4]

    # Atleast one mine clause

    mine_exist=[]
    for i in range(16): 
        mine_exist.append(i+1)
    knowledge_base.add_clause(mine_exist)

    # Atleast one mine clause

    ## Entering knowledge about =0 percept

    for i in range(4):
        for j in range(4):
            neighbours=[]
            if i>0 :
                neighbours.append([i-1,j])
            if i<3 :
                neighbours.append([i+1,j])            ## Used statement (=0[x,y] implies not a single mine in neighbouring fields)
            if j>0 :
                neighbours.append([i,j-1])
            if j<3 :
                neighbours.append([i,j+1])
            for k in neighbours:
                knowledge_base.add_clause([(-literals["M"+str(k[0]+1)+str(k[1]+1)]),(-literals["=0"+str(i+1)+str(j+1)])])

    ## =0 percept knowledge finished


    ## Entering knowledge about =1 percept

    for i in range(4):
        for j in range(4):
            neighbours=[]
            if i>0 :
                neighbours.append([i-1,j])
            if i<3 :
                neighbours.append([i+1,j])
            if j>0 :
                neighbours.append([i,j-1])
            if j<3 :
                neighbours.append([i,j+1])         ## Used statement (=1[x,y] implies only one mine in neighbouring fields considering all possibilities)
        
            for k in neighbours:
                for l in neighbours:
                    if(k!=l):
                        knowledge_base.add_clause([(-literals["M"+str(l[0]+1)+str(l[1]+1)]),(-literals["M"+str(k[0]+1)+str(k[1]+1)]),(-literals["=1"+str(i+1)+str(j+1)])])

            temp=[]     
            for k in neighbours:
                temp.append(literals["M"+str(k[0]+1)+str(k[1]+1)])

            temp.append((-literals["=1"+str(i+1)+str(j+1)]))
            knowledge_base.add_clause(temp)

    ## =1 percept knowledge finished

    ## Entering knowledge about >1 percept

    for i in range(4):
        for j in range(4):
            neighbours=[]
            if i>0 :
                neighbours.append([i-1,j])
            if i<3 :
                neighbours.append([i+1,j])
            if j>0 :
                neighbours.append([i,j-1])
            if j<3 :
                neighbours.append([i,j+1])

      
            for k in neighbours:
                temp=[]
                for l in neighbours:
                    if(l!=k):
                        temp.append((literals["M"+str(l[0]+1)+str(l[1]+1)]))     ## Used statement (>1[x,y] implies atleast two mines in neighbouring fields considering all possibilities)

                temp.append(-(literals["M"+str(k[0]+1)+str(k[1]+1)]))
                temp.append(-(literals[">1"+str(i+1)+str(j+1)]))
                knowledge_base.add_clause(temp)

            temp=[]     
            for k in neighbours:
                temp.append(literals["M"+str(k[0]+1)+str(k[1]+1)])

            temp.append((-literals[">1"+str(i+1)+str(j+1)]))
            knowledge_base.add_clause(temp)

    ## >1 percept knowledge finished
    
    ag = Agent()                                     # Initializing a world where agent exists with mines in the world
    path_travelled=[]                                # list denoting the path travelled by agent
    print("Feed of movements done by the agent:\n")
    print("Starting location of agent:",ag.FindCurrentLocation())
    path_travelled.append(ag.FindCurrentLocation())
    init_source=[1,1]
    safe_to_travel.append([1,1])
    while(True):

        if(init_source==[4,4]):
            break
        
        visited = []
        
        safe_to_travel.remove(init_source)
        safe_explored.append(init_source)
        x_coord=ag.FindCurrentLocation()[0]
        y_coord=ag.FindCurrentLocation()[1]
        knowledge_base.add_clause([literals[ag.PerceiveCurrentLocation()+str(x_coord)+str(y_coord)]])   # Entering the percept of the current location of the agent

        for i in range(4):
            for j in range(4):
              if not (knowledge_base.solve(assumptions=[literals["M"+str(i+1)+str(j+1)]])):
                  knowledge_base.add_clause([-literals["M"+str(i+1)+str(j+1)]])                         # Making an inference on all the locations that if they contain a mine or not or nothing can be determined as of now
              if not (knowledge_base.solve(assumptions=[-literals["M"+str(i+1)+str(j+1)]])):
                  knowledge_base.add_clause([literals["M"+str(i+1)+str(j+1)]])
      

        for i in range(4):
            for j in range(4):
              if not (knowledge_base.solve(assumptions=[literals["M"+str(i+1)+str(j+1)]])):
                    if ([i+1,j+1]) not in safe_to_travel and ([i+1,j+1]) not in safe_explored:         # Adding newly discovered safe locations if found any with our recent inference
                      if [i+1,j+1] != [4,4]:
                        safe_to_travel.append([i+1,j+1])

        
        min_distance=100
        destination=[-1,-1]

        
        if i<4 :
            if(init_source[0]+1==4 and init_source[1]==4):
                safe_to_travel.append([4,4])
        if j<4 :
            if(init_source[0]==4 and init_source[1]+1==4):
                safe_to_travel.append([4,4])

        for i in safe_to_travel:
            if((8-(i[0]+i[1]))<min_distance):
                destination[0]=i[0]
                destination[1]=i[1]
                min_distance=(8-(i[0]+i[1]))


        queue = []
        path = []
        queue.append(init_source)

        ## BFS START

        while(True):

            if(not queue):
              print("No further inference can be made to move towards goal hence goal state cant be reached")
              return 0;

            co_ord=queue.pop(0)

            visited.append(co_ord)
            
            if(co_ord == destination):
                curr = destination
                while(curr != init_source):

                    if(curr[0] == parent_node[str(curr[0])+str(curr[1])][0]+1):
                        path.append('Right')
                    if(curr[0] == parent_node[str(curr[0])+str(curr[1])][0]-1):
                        path.append('Left')
                    if(curr[1] == parent_node[str(curr[0])+str(curr[1])][1]+1):                         ## APPLYING BFS (Breadth first search) ALGORITHM TO FIND PATH TRAVELLED BY AGENT
                        path.append('Up')
                    if(curr[1] == parent_node[str(curr[0])+str(curr[1])][1]-1):
                        path.append('Down')
                
                    curr=parent_node[str(curr[0])+str(curr[1])]

                break

            if co_ord[0]>1 and ([co_ord[0]-1,co_ord[1]] in safe_explored or [co_ord[0]-1,co_ord[1]] in safe_to_travel) and [co_ord[0]-1,co_ord[1]] not in visited:
                queue.append([co_ord[0]-1,co_ord[1]])
                parent_node[str(co_ord[0]-1)+str(co_ord[1])]=co_ord

            if co_ord[0]<4 and ([co_ord[0]+1,co_ord[1]] in safe_explored or [co_ord[0]+1,co_ord[1]] in safe_to_travel) and [co_ord[0]+1,co_ord[1]] not in visited:
                queue.append([co_ord[0]+1,co_ord[1]])
                parent_node[str(co_ord[0]+1)+str(co_ord[1])]=co_ord

            if co_ord[1]>1 and ([co_ord[0],co_ord[1]-1] in safe_explored or [co_ord[0],co_ord[1]-1] in safe_to_travel) and [co_ord[0],co_ord[1]-1] not in visited:
                queue.append([co_ord[0],co_ord[1]-1])
                parent_node[str(co_ord[0])+str(co_ord[1]-1)]=co_ord

            if co_ord[1]<4 and ([co_ord[0],co_ord[1]+1] in safe_explored or [co_ord[0],co_ord[1]+1] in safe_to_travel) and [co_ord[0],co_ord[1]+1] not in visited:
                queue.append([co_ord[0],co_ord[1]+1])
                parent_node[str(co_ord[0])+str(co_ord[1]+1)]=co_ord
            
    
        ## BFS END

        path.reverse()
        for i in path:
            ag.TakeAction(i)
            path_travelled.append(ag.FindCurrentLocation())
            if(ag.FindCurrentLocation() in safe_to_travel):      ## Travelling on the path that is discovered for agent
              safe_explored.append(ag.FindCurrentLocation())
        init_source=destination

    print("Destination reached safely\n")

    print("Path followed by agent to reach destination")
    for i in range(0,len(path_travelled)-1):
      print(path_travelled[i],end=' ')
      print('-->',end=' ')
    print(path_travelled[len(path_travelled)-1])

if __name__=='__main__':
    main()
