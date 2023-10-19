import os
import random
import json
from subs import fetch_server,task
current_directory = os.path.dirname(__file__)

parent_directory = os.path.dirname(current_directory)

servers_path = os.path.join(parent_directory, 'subserver/servers.json')

#with open(servers_path, 'r') as json_file:
    #server_data = json.load(json_file)

class MasterServer:
    def __init__(self,ID):
        self.ID = ID

    def masterserver(self,file,GPU,RAM):
        #user_gpu=GPU
        #user_ram=RAM

        server_data = fetch_server(GPU)
        
        total_weight = sum(weight for server, weight in server_data)

        def job_complexity(file_path):
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            return data[0]["complexity_level"]
        
        #json_directory =  "./Jas-os-app/"
        #file_path = os.path.join(json_directory, file)
        file_path = os.getcwd(file)
        jobCom = job_complexity(file_path)

        selected_server = None
        current_weight = 0
        while selected_server is None:
            for server, weight in server_data:
                current_weight += weight + jobCom  
            if current_weight >= random.randint(1, total_weight):
                selected_server = server
                break 

        task(GPU,selected_server,file_path) 
        #return selected_server
    
    
    def call_sub(self,selected_server):
        selected_server.subserver()