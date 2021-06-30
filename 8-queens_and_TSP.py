import copy
import random
from matplotlib import pyplot as plt

print("AI_Assignment 2018A7PS0637G")
print("Enter q for solving 8-queens or enter t for solving TSP")

query=input()

if query=="q" or query=="Q":
#Question 1 starts

  #FITNESS function starts
  def fitness(curr_list):
      max_fitness_value=0
      for i in range(len(curr_list)):
          for j in range(i+1,len(curr_list)):
              if(curr_list[i]==curr_list[j] or abs(curr_list[i]-curr_list[j])==abs(i-j)): #queens either lying in the same row or lying at a diagonally crossing position then fitness will be decremented
                  max_fitness_value+=1
      return(29-max_fitness_value) #fitness value of state being considered
  #FITNESS function ends

  generations = 1000                #number of generations being considered
  population_size = 50
  init_state = []
  for i in range(0,8):
      init_state.append(1)          # 


  population = []
  for i in range(0,population_size):
      population.append(init_state) # initializing population with all fitness values 1 of every queen



  mutation_probability=0.98
  max_fitness_value_answer=0 # max_fitness obtained out of all generations
  best_fitness = [] # List consisting of max_fitness for every generation
  max_fitness_seq = [] # position of the queens columnwise(i.e each index represents the column of the corresponding queen and value represents row in which queen is present) corresponding to maximum fitness

  #ITERATION for generation starts
  for i in range (generations):

      new_population = []
      max_fitness_value=0 # max_fitness obtained in the current generation
      for it in range(0,len(population)):
          weight=[]                                     # weight being applied to each population which is in direct proportion with fitness
          for j in range(0,len(population)):
            weight.append(1.5**fitness(population[j]))  # HEURISTIC (Exponentiating weights helps choosing better value stochastically thus improving algorithm)

          # REPRODUCTION starts
          x = random.choices(population,weight)[0] # stochastically choosing two parents with weight being applied in choosing
          y = random.choices(population,weight)[0]
          reproduced =[]
          z=random.randint(1,7) # choosing random index which will be the breakpoint for reproduction
          for j in range (0,z):
              reproduced.append(x[j]) 
          for j in range (z,8):         # Reproduction
              reproduced.append(y[j])
          # REPRODUCTION ends

          # MUTATION Starts
          if random.uniform(0,1)>=mutation_probability:
              point_for_mutation=random.randint(0,7) # Randomly choosing the index that is to be mutated
              val = reproduced[point_for_mutation]
              choice_value = []                      # HEURISTIC:->
              choice_of_mutation = []                # Here Choice_value list signifies what all values can be considered for the mutation for the chosen index (i.e all the values except the value present at that index)
              for k in range(1,9):                   # Choice_of_mutation list takes in all mutated lists that are possible by taking each value from choice_value list
                if(k!=val):
                  choice_value.append(k)
              for k in range(0,len(choice_value)):                      # Code for creating the choice_of_mutation list
                choice_of_mutation.append(copy.deepcopy(reproduced))
              for k in range(0,len(choice_value)):
                choice_of_mutation[k][point_for_mutation]=choice_value[k]
                                                                        # Code ends
              weight_for_mutation = []
              for k in choice_of_mutation:
                weight_for_mutation.append(fitness(k))                   # Giving weight to every list in choice_of_mutation according to fitness value of each list in choice_of_mutation
              mutated=random.choices(choice_of_mutation,weight_for_mutation)[0] #stochastically choosing the mutated child obtained from parents (Thus giving a stochastically better mutated list with better fitness value)
              reproduced=mutated
          #MUTATION ends
          new_population.append(reproduced) # Mutated child inserted in new_population

          if(fitness(reproduced)>max_fitness_value_answer):
            max_fitness_value_answer=fitness(reproduced)                
            max_fitness_seq=reproduced

          max_fitness_value=max(max_fitness_value,fitness(reproduced))
          if max_fitness_value==29:
              break
      population = new_population
      best_fitness.append(max_fitness_value)
      if(max_fitness_value==29):
          break

  print("Best fitness value",max_fitness_value_answer)
  print("Best fitness value sequence",max_fitness_seq)
  plt.xlabel("generations")
  plt.ylabel("best_fitness_value")
  plt.plot(best_fitness)
  plt.title("Best fitness value of each generation")
  plt.show()
# Question1 ends

elif query=="t" or query=="T":

  city_dist_matrix = [[0,1000,1000,1000,1000,1000,0.15,1000,1000,0.2,1000,0.12,1000,1000],
      [1000,0,1000,1000,1000,1000,1000,0.19,0.4,1000,1000,1000,1000,0.13],
      [1000,1000,0,0.6,0.22,0.4,1000,1000,0.2,1000,1000,1000,1000,1000],
      [1000,1000,0.6,0,1000,0.21,1000,1000,1000,1000,0.3,1000,1000,1000],
      [1000,1000,0.22,1000,0,1000,1000,1000,0.18,1000,1000,1000,1000,1000],
      [1000,1000,0.4,0.21,1000,0,1000,1000,1000,1000,0.37,0.6,0.26,0.9],
      [0.15,1000,1000,1000,1000,1000,0,1000,1000,1000,0.55,0.18,1000,1000],
      [1000,0.19,1000,1000,1000,1000,1000,0,1000,0.56,1000,1000,1000,0.17],         # Matrix stating distance between cities pairwise (0 for distance of city from itself)
      [1000,0.4,0.2,1000,0.18,1000,1000,1000,0,1000,1000,1000,1000,0.6],            # Infinite distance is given value of 1000 for calculating purposes
      [0.2,1000,1000,1000,1000,1000,1000,0.56,1000,0,1000,0.16,1000,0.5],
      [1000,1000,1000,0.3,1000,0.37,0.55,1000,1000,1000,0,1000,0.24,1000],
      [0.12,1000,1000,1000,1000,0.6,0.18,1000,1000,0.16,1000,0,0.4,1000],
      [1000,1000,1000,1000,1000,0.26,1000,1000,1000,1000,0.24,0.4,0,1000],
      [1000,0.13,1000,1000,1000,0.9,1000,0.17,0.6,0.5,1000,1000,1000,0]]

  def fitness1(curr_perm):
    max_fitness_value1 =0
    for i in range(len(curr_perm)-1):
      max_fitness_value1 +=city_dist_matrix[curr_perm[i]][curr_perm[i+1]]            # Fitness functon of TSP takes in a permutation of Alphabets (denoted by integers in the program A->0,B->1....,N->13)
    max_fitness_value1 +=city_dist_matrix[curr_perm[len(curr_perm)-1]][curr_perm[0]] # From the City_dist matrix it calculates distance between adjacent cities in the permutation and sums it up (distance of the hamiltonian walk) 
    return 1/max_fitness_value1                                                      # We consider 1/(distance of walk) as our fitness function


  generations = 1500                                                                 # Number of generations we are considering
  population_size = 50                                                               # Population size given value of 50


  init_state = []
  for i in range(0,14):                                                              # Initializing every state in population with the permutation A,B,C,.....N (i.e 0,1,2,3,.....13)
      init_state.append(i)

  population = []

  for i in range(0,population_size):
      population.append(init_state)

  max_fitness_value1_answer = 0 # max_fitness obtained out of all generations
  max_fitness_seq1 = [] # Permutation of cities (i.e the walk TSP algorithm followed) corresponding to the maximum fitness value
  best_fitness1 = []    # List consisting of max_fitness for every generation
  mutation_probability=0.98
  for zz in range (generations):
      new_population = []    # New population generated with mutation and reproduction carried out in previous population
      max_fitness_value1 = 0 # max_fitness obtained in the current generation
      for i in range(0,len(population)):
          weight=[]
          for j in range(0,len(population)):
            weight.append(fitness1(population[j]))                                  # Weight being applied to each population which is in direct proportion with fitness
          x = random.choices(population,weight)[0]                                  # Parent 1 stochastically chosen
          y = random.choices(population,weight)[0]                                  # Parent 2 stochastically chosen

          #REPRODUCTION STARTS                                  
          reproduced =[14,14,14,14,14,14,14,14,14,14,14,14,14,14]                   
          z1=random.randint(0,13)                                    
          z2=random.randint(0,13)                                    # the two indices (i.e z1 and z2) are the indices between which our subset will be chosen
          for j in range (min(z1,z2),max(z1,z2)+1):
              reproduced[j]=x[j]

          k=0
          for j in range (14):                                       # Remaining elements to be positioned as they were in the original permutation excluding the subset we have chosen (following the given algorithm stated in the pdf)
              if(y[j] not in reproduced):
                while(reproduced[k]!=14 and k<14):
                  k+=1
                reproduced[k]=y[j]
                k+=1
          #REPRODUCTION ENDS

          #STANDARD MUTATION FUNCTION:->
          if random.uniform(0,1)>=mutation_probability:                                                     
            point_for_mutation1 = random.randint(0,13)
            point_for_mutation2 = random.choice([i for i in range(0,14) if i not in [point_for_mutation1]]) # Considering two indices which will be selected randomly for swapping
            swap1 = reproduced[point_for_mutation1]
            swap2 = reproduced[point_for_mutation2]                 
            reproduced[point_for_mutation1]=swap2
            reproduced[point_for_mutation2]=swap1                                                           # swapping the values from corresponding indices chosen and hence mutation occurs




          # OPTIMIZED MUTATION FUNCTION :-> #(Here we are finding two edges in the walk with maximum distance (i.e first edge with maximum distance and second edge with maximum distance having no common edge with first one))
                                            #(and after finding such two edges we delete those edges from walk and add their crossing edges (Basically swapping two cities that we have found))
          if random.uniform(0,1)>=mutation_probability:

            ind1 = -1 # Index1 which will be considered for swapping
            ind2 = -1 # Index2 which will be considered for swapping
            max_val_city2 = 0   # Here this variable stores maximum distance found of the second city having no common edge with the first city
            for j in range(len(reproduced)-1):
              if city_dist_matrix[reproduced[j]][reproduced[j+1]]==1000:  
                ind1=j                     
                break                                                           # this code snippet calculates the first index of the city which is having infinity distance (i.e two cities that are not connected)
            if city_dist_matrix[reproduced[(len(reproduced)-1)]][reproduced[0]]==1000 and ind1==-1:
                ind1=(len(reproduced)-1)

            if ind1!=-1:                                                        # if index1 is found then only we will have to find index2 otherwise if index1=-1 it means all cities are connected in the walk which requires no mutation
              not_to_take = [reproduced[ind1]]
              if ind1==0:
                not_to_take.append(reproduced[len(reproduced)-1])
                not_to_take.append(reproduced[1])
              elif ind1==len(reproduced)-1:                                     # Here not_to_take list consists of all such cities that cannot be considered for choosing the second index (i.e index2)
                not_to_take.append(reproduced[len(reproduced)-2])
                not_to_take.append(reproduced[0])
              else:
                not_to_take.append(reproduced[ind1+1])
                not_to_take.append(reproduced[ind1-1])

              for j in range(len(reproduced)-1):
                if reproduced[j] not in not_to_take:
                  if max_val_city2<city_dist_matrix[reproduced[j]][reproduced[j+1]]:      # Here ind2 represents the city which is having maximum adjacent distance and not having any common edge with city ind1
                    max_val_city2=city_dist_matrix[reproduced[j]][reproduced[j+1]]
                    ind2=j
              if reproduced[len(reproduced)-1] not in not_to_take:
                if max_val_city2<city_dist_matrix[reproduced[len(reproduced)-1]][reproduced[0]]:
                    max_val_city2=city_dist_matrix[reproduced[len(reproduced)-1]][reproduced[0]]
                    ind2=len(reproduced)-1

              reproduced[ind1],reproduced[ind2]=reproduced[ind2],reproduced[ind1]         # Swapping the two cities (basically removing the chosen two paths and adding their crossovers)

          new_population.append(reproduced)

          if fitness1(reproduced)>max_fitness_value1_answer:
            max_fitness_value1_answer = fitness1(reproduced)
            max_fitness_seq1 = reproduced

          max_fitness_value1=max(max_fitness_value1,fitness1(reproduced))

      best_fitness1.append(max_fitness_value1)
      population = new_population

  print("Best fitness value",1/max_fitness_value1_answer)
  print("Best fitness value sequence",max_fitness_seq1)
  plt.xlabel("generations")
  plt.ylabel("best_fitness_value")
  plt.plot(best_fitness1)
  plt.title("Best fitness value of each generation")
  plt.show()

else:
  print("Invalid query") 