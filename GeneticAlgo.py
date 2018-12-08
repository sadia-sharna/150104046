# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 19:27:28 2018

@author: tshar
"""


import random
from itertools import permutations

def generate_random_permutation(combination = '0123456789'):
    """Generates a random permutation of given combination string.
    Keyword arguments:
    combination -- the input string to be permuted(default "0123456789")
    returns a random permutation
    """
      
    # Get all permutations of string combination
    perms = permutations(combination)
    permList = list(perms)
    chromosome=[]
    for i in range(0,10):
        idx=(random.randint(0,len(permList)))
        removecomma = ''.join(permList[idx])
        chromosome.append(removecomma)
    
    return chromosome

def fitness_function(combination):
    """calculates the fitness of a given state, i.e.- number of non-attacking queen pairs
    Keyword arguments:
    combination- input state
    
    returns the fitness/ number of non-attacking pairs in this case 
    """
    fitness = 45 #non-attacking pairs //nC2,n=10,r=2

    for i in range(0,9):
        for j in range(i+1,10):

            #if abs(i-j) == abs( int(combination[i])- int(combination[j])):
            if abs(i-j) == abs( int(combination[i])- int(combination[j])) or (abs( int(combination[i])- int(combination[j]))==2 and abs(i-j)==1) or (abs( int(combination[i])- int(combination[j]))==1 and abs(i-j)==2):
                fitness -= 1 #one attacking pair found
    return fitness
    
def rank_selection(chromosome):

    fitnessList=[][:]
    checkIndexList=[]
        
    for i in range(0,10):
        j = fitness_function(chromosome[i])
        fitnessList.append(j) #jotogula chromosome ache tader fitness ekta list e rakhchi
    print('Fitness List of 10 population : ')
    print(fitnessList)
    
    sortedFitnessList = fitnessList.copy()
    sortedFitnessList.sort(reverse=True) #highest to lowest order e
    r=0
    rank=fitnessList.copy()
    for i in range(0,10):
        for j in range(0,10):
            if sortedFitnessList[i]==fitnessList[j] and j not in checkIndexList:#jodi same fitness koyekbar thake
                r+=1
                rank[j]=r
                checkIndexList.append(j) #age assign kora hoyeche kina
                if i==0:
                    first_parent_pos=j+1
                elif i==1:
                    second_parent_pos=j+1
                break
    parentOne=main_chromosome[first_parent_pos-1]
    parentTwo=main_chromosome[second_parent_pos-1]
    print('Sorted fitness list : ')
    print(sortedFitnessList)
    print('Rank list according to the sorted fitness list : ')
    print(rank)
    print('First Parent position : ')
    print(first_parent_pos)
    print('Second Parent position : ')
    print(second_parent_pos)
        
    return parentOne,parentTwo


def cycle_by_index(First_parent,Second_parent,ind,li):
    flag=0
    i=ind
    count=0
    if ind not in li:
      flag=1   
      while First_parent[ind]!=Second_parent[i] :
        li.append(i) #index gulo first parent er ekta list e rakhchi
        count+=1 #protibar koyta element list e add hocche
        cyclic_term=First_parent[i]
        if cyclic_term != Second_parent[i]:
           search= First_parent.index(Second_parent[i]) #First parent er value er index search korchi
           i=search
      if i not in li and First_parent[ind]==Second_parent[i]: #jodi matching thake ek index e 2 parent er value sheiijonno
         li.append(i)
         count+=1
    return li,flag,count
    

def cycle_crossover(First_parent,Second_parent):
   total_count=0
   cross_or_not=0
   lis=[]
   newParentOne=[0,0,0,0,0,0,0,0,0,0]
   newParentTwo=[0,0,0,0,0,0,0,0,0,0]
   for index in range(0,len(First_parent)):
       lis,flag,count=cycle_by_index(First_parent,Second_parent,index,lis)
      
       if flag==1 :
          cross_or_not+=1
          if cross_or_not % 2 ==0 : #ekbar change hbe,ekbar hbena
              for i in range(total_count,total_count+count):
                  newParentOne[lis[i]] = Second_parent[lis[i]]
                  newParentTwo[lis[i]] = First_parent[lis[i]]
          else:
               for i in range(total_count,total_count+count):
                  newParentOne[lis[i]] = First_parent[lis[i]]
                  newParentTwo[lis[i]] = Second_parent[lis[i]]
          total_count=total_count+count  
          
   return  newParentOne,newParentTwo


def scramble_mutation(parentOne,parentTwo):
     first_value= random.randint(0,len(parentOne)//2) #2 ta value select korla ekta range erjonno,jei range e change korbo
     second_value= random.randint((len(parentOne)//2),len(parentOne))
     #dif=abs(first_value-second_value)
     li_1=parentOne.copy()
     permsone = permutations(li_1[first_value:second_value]) #selected part e permutation 
     permListone=list(permsone)
     newparentone=li_1.copy()
     i=random.randint(0,len(permListone)) #permutation gular jekono ekta value select randomly
     newparentone[first_value:second_value]=permListone[i] #oituku part change kore dilam
     
     li_2=parentTwo.copy()
     permstwo = permutations(li_2[first_value:second_value])
     permListtwo=list(permstwo)
     newparenttwo=li_2.copy()
     i=random.randint(0,len(permListtwo))
     newparenttwo[first_value:second_value]=permListtwo[i]
     return newparentone,newparenttwo
     
def printBoard(combination):
    """Prints the chessboard.

    Keyword arguments:
    combination -- a string denoting which row contains queens in which column
    
    """
    #board to be print, dimension 8X8
    board_array = []
    #Filling the board with *
    for i in range(0,10):
        board_array.append([])
        for j in range(0,10):
            board_array[i].append("*")
    #Placing queens in the board based on input combination
    for i in range(len(combination)):
        board_array[i][int(combination[i])-1] = "Q" 
    for i in range(0,10):
        print(board_array[i])     
   
if __name__ == "__main__":
    
    random.seed()
    print("Solving 10 super queen problem with genetic algorithm\n")
    
    main_chromosome=generate_random_permutation() #main func er chromosome means possible solution
    
    print('Total Popultaion \n')
    print(main_chromosome)
    
    print('\n\n## Rank Selection ##\n\n')
          
    first_parent,second_parent=rank_selection(main_chromosome)
    
    print('First Parent that has been Selected by Rank Selection:\n')
    print(first_parent)
    print('Second Parent that has been Selected by Rank Selection:\n')
    print(second_parent)
    
    newparentone,newparenttwo=cycle_crossover(first_parent,second_parent)
    
    print('\n\n## Cycle Cross Over ##\n\n')
    
    print('First Child After Cyclic Cross Over :\n')
    print(''.join(newparentone))
    print('Second Child After Cyclic Cross Over:\n')
    print(''.join(newparenttwo))
    
    print('\nFitness of child one and two\n')
    print('First Child')
    print(fitness_function(newparentone))
    print('Second Child')
    print(fitness_function(newparenttwo))
    
    print('\n\n## Scramble Mutation ##\n\n')
    mutated_childone,mutated_childtwo=scramble_mutation(newparentone,newparenttwo)
    
    print('First Parent After Scramble Mutation:\n')
    print(''.join(mutated_childone))
    printBoard(mutated_childone) 
    print('\nSecond Parent After Scramble Mutation:\n')
    print(''.join(mutated_childtwo))
    printBoard(mutated_childtwo)
    print('\nFitness of child one and two\n')
    print('First Child')
    print(fitness_function(mutated_childone))
    print('Second Child')
    print(fitness_function(mutated_childtwo))
    
    
    

