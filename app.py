# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:58:26 2020

@author: User
"""
from flask import Flask, jsonify
from flask_restful import Resource, Api
import subprocess
#from NSGAIII import transform
#from flask-jsonpify import jsonify
app = Flask(__name__)
api = Api(app)

class fct(Resource):
    def get(self):
        
        cmd = ('docker-machine ssh Manager docker stack deploy --compose-file Monitoring-Docker-Swarm/cbe-app.yml p1').split()

        p = subprocess.Popen(cmd,stdout = subprocess.PIPE)
        output, errors = p.communicate()
       
        print(output)
        print(errors)
        result=jsonify("done")
       
        return (result)
class fct1(Resource):
    def get(self):
        #transform()
        cmd = ('docker-machine ssh Manager docker stack deploy --compose-file Monitoring-Docker-Swarm/final.yml p1').split()

        p = subprocess.Popen(cmd,stdout = subprocess.PIPE)
        output, errors = p.communicate()
       
        print(output)
        print(errors)
       
        result=jsonify("done")
       
        return (result)    
    
    
        
        
api.add_resource(fct, '/fct') # Route_1
api.add_resource(fct1, '/fct1')

#
#
if __name__ == '__main__':
     app.run(port='5002')        