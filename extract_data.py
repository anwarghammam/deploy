# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 13:11:51 2020

@author: User
"""

import subprocess
import json

all1={}
import yaml

#NUMBER OF NODES BY CLUSTER 



#manager="manager2"
def create_machines():
    machines=[]
    with  open(r"C:\Users\User\Desktop\test3.txt",'w') as file :
    
    
        cmd = ('docker-machine ssh manager1 docker node ls').split()

        p = subprocess.Popen(cmd,stdout=file)
        output, errors = p.communicate()


    with open(r"C:\Users\User\Desktop\test3.txt",'r') as file:
    
    
        for line in file:
    
            line=line.replace("*",'')
          
        
            groupe=line.split()
          
            machines.append(groupe[1])
   
    machines[0]='manager1'  
    del machines[1]
    return machines

def create():
    machines=create_machines()
    containers=[]
    initial_state=[]
    for i,machine in enumerate(machines) :
        containers1=[]
        with  open(r"C:\Users\User\Desktop\test3.txt",'w') as file :
            cmd = ('docker-machine ssh '+str(machine)+' docker ps ').split()

            p = subprocess.Popen(cmd,stdout=file)
            output, errors = p.communicate()
        with open(r"C:\Users\User\Desktop\test3.txt",'r') as file:
        
            for line in file:
            
                groupe=line.split()
           
                containers1.append(groupe[1])
            
        containers1=containers1[1:] 
        print("avant")
        print(containers1)
       
        if( 'stefanprodan/swarmprom-node-exporter:v0.16.0' in containers1):
            del containers1[containers1.index('stefanprodan/swarmprom-node-exporter:v0.16.0')]
        if( 'cloudflare/unsee:v0.8.0' in containers1): 
            
            del containers1[containers1.index('cloudflare/unsee:v0.8.0')]
        if('stefanprodan/swarmprom-prometheus:v2.5.0' in containers1):       
            del containers1[containers1.index('stefanprodan/swarmprom-prometheus:v2.5.0')]
        if('google/cadvisor:latest' in containers1):   
            del containers1[containers1.index('google/cadvisor:latest')]
        if('stefanprodan/caddy:latest' in containers1):   
            del containers1[containers1.index('stefanprodan/caddy:latest')]
        if('stefanprodan/swarmprom-grafana:5.3.4' in containers1):   
            del containers1[containers1.index('stefanprodan/swarmprom-grafana:5.3.4')]
        if('stefanprodan/swarmprom-alertmanager:v0.14.0' in containers1):   
            del containers1[containers1.index('stefanprodan/swarmprom-alertmanager:v0.14.0')]
        if('stefanprodan/caddy:latest' in containers1):   
            del containers1[containers1.index('stefanprodan/caddy:latest')]    
            
            
        print("apres")
        print(containers1)
     
   
        for container in containers1:
        
            containers.append(container)
            initial_state.append(i)        
        
       
    machines[0]='boot2docker'   
   
    
   
    
    return containers,initial_state,machines



def keep_trace1(containers,state,machines,file1=r'C:\Users\User\Desktop\docker\docker-compose.yml'):
    with open(r'C:\Users\User\Desktop\docker\docker-compose.yml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
        compose = yaml.load(file)
        
    
    for i,con  in enumerate(containers) :
        for dict in compose['services']:
            
            
            if str(compose['services'][dict]['image']) in str(con):
                
                name='node.hostname == '+str(machines[state[i]])
                compose['services'][dict].update({'deploy': {'placement': {'constraints':  [ name ]}}})    
                
 
    with open(file1,'w') as file1:
        
        yaml.dump(compose,file1)  
containers ,initial_state,machines=create()
print(containers)
print(initial_state)
def keep_trace2():
    all3=[]
    with open(r'C:\Users\User\Desktop\docker\docker-compose.yml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
        compose = yaml.load(file)
        print(containers)
        for dict in compose['services']:
            
            if((compose['services'][dict].get('depends_on') is not None)):
                image=compose['services'][dict]['image']
                for k,con in enumerate(containers):
                    if (str(image) in str(con)) :
                        key=k
                        print(key)
                        
                
                dependencies=compose['services'][dict]['depends_on']
                images=[]
                for dep in dependencies:
                    images.append(compose['services'][dep]['image'])
                for dep in images:
                    for j,con in enumerate(containers):
                        if (str(dep) in str(con)) and ((key,j) not in all3):
                            all3.append((key,j))
                
               
                            
             
            if((compose['services'][dict].get('links') is not None)):
                image=compose['services'][dict]['image']
                for k,con in enumerate(containers):
                    if (str(image) in str(con)):
                        key=k
                        print(key)
                        
                
                dependencies=compose['services'][dict]['links']
                images=[]
                for dep in dependencies:
                    images.append(compose['services'][dep]['image'])
                for dep in images:
                    for j,con in enumerate(containers):
                        if (str(dep) in str(con)) and  ((key,j) not in all3):
                            all3.append((key,j))
        print(all3)    
        return all3   


    