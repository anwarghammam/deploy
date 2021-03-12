# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 12:13:49 2020

@author: User
"""


from abc import ABC
from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
import collections
from extract_data import create , keep_trace1,keep_trace2



containers,initial_state,machines=create()
keep_trace1(containers,initial_state,machines)
n_nodes=3
class MOOC(IntegerProblem,ABC):
    """ Problem MOOC.
    .. note::  The default number of variables is 30.
    .. note:: Continuous problem having a convex Pareto front
    """

    def __init__(self, number_of_variables: int=len(containers)):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(MOOC, self).__init__()
        self.dependencies=keep_trace2()
        self.initial_state=initial_state
        self.number_of_variables = len(containers)
        self.number_of_objectives = 5
        self.number_of_constraints =0

        self.obj_directions = [self.MINIMIZE,self.MINIMIZE,self.MAXIMIZE,self.MINIMIZE,self.MINIMIZE]
        self.obj_labels = ['nb_nodes','max_nb_containers_per_node','cohesion','coupling','nb_changes']

        self.lower_bound = self.number_of_variables * [0.0]
        self.upper_bound = self.number_of_variables * [n_nodes-1]
    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        
        nb_nodes= self.eval_number_nodes(solution)
        nb_containers_per_node= self.eval_nb_containers_per_node(solution)
        cohesion,coupling=self.eval_cohesion_coupling(solution)
        nb_changes=self.eval_nb_changes(solution)
        

        solution.objectives[0] = nb_nodes
        solution.objectives[1] = nb_containers_per_node
        solution.objectives[2]=-1*cohesion
        solution.objectives[3]=coupling
        solution.objectives[4]=nb_changes
        
     
        return solution

#    def __evaluate_constraints(self, solution: IntegerSolution) -> None:
#        constraints = [0.0 for _ in range(self.number_of_constraints)]
#
#        constraints[0] = 2
#        
#
#        solution.constraints = constraints

       
    
    
    def eval_number_nodes(self, solution: IntegerSolution):
        nb_nodes = len(set(solution.variables))

        

        return nb_nodes

    def eval_nb_containers_per_node(self, solution: IntegerSolution):
        
        occurences=[]
    
        for val in collections.Counter(solution.variables).values() :
            
            occurences.append(val)
            average =sum(occurences)/ len(occurences)
      
        return (average)
    def eval_cohesion_coupling(self,solution:IntegerSolution):
        
        intra_dependencies=0
        inter_dependencies=0
        for dep in self.dependencies:
            if(solution.variables[dep[0]]==solution.variables[dep[1]]):
                intra_dependencies+=1
            else :
                 inter_dependencies+=1
        return  intra_dependencies,inter_dependencies
    def eval_nb_changes(self ,solution:IntegerSolution)   :
        changes=0
        initial_set=set(self.initial_state)
        solution_set=set(solution.variables)
        for i in initial_set:
            if i not in solution_set:
                changes+=1
#        for i in solution_set:
#            if i not in initial_set:
#                changes+=1        
        for i in range(len(self.initial_state)):
            if (self.initial_state[i]!=solution.variables[i]):
                changes+=2
                
        return(changes)        
        
        
    def get_name(self):
        return 'MOOC'    