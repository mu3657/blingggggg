import random
import os
import time
import multiprocessing
import tqdm
import json
import sys
import cmd
import subprocess
import re
import logging



class GPU:
    def __init__(self, identifier, model, region, servers, vram, num_compute_units):
        self.identifier = identifier
        self.model = model
        self.vram = vram
        self.num_compute_units = num_compute_units
        self.region = region
        self.servers = servers
        self.is_available = True

    def allocate(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    def release(self):
        self.is_available = True


class GPUPool:
    def __init__(self, gpus):
        self.gpus = gpus

    def allocate_gpu(self, task_id):
        for gpu in self.gpus:
            if gpu.allocate():
                print(
                    f"Task {task_id} allocated to GPU {gpu.model} with {gpu.vram}MB VRAM and {gpu.num_compute_units} compute units.")
                return
        print(f"No available GPU for task {task_id}")

    def release_gpu(self, task_id):
        for gpu in self.gpus:
            if not gpu.is_available:
                gpu.release()
                print(f"Task {task_id} released GPU {gpu.model}")
                return
        print(f"Task {task_id} not found in GPU allocation")


found_server1 = []
found_server2 = []
found_server3 = []
found_server4 = []
server_instances = []


    # p = multiprocessing.Pool(3)
    # for i in range(1, 3):
    #     p.apply_async(job, args=())
    # p.close()
    # p.join()
queue = multiprocessing.Queue()

progress_queue= multiprocessing.Queue()
# aaa

class SubServers:
    def __init__(self,name,ID,GPU,weight,availiable_ram,availiable):
        self.name = name
        self.subID = ID
        self.GPU = GPU
        self.weight = weight
        self.availiable_ram = availiable_ram
        self.availiable = availiable
def fetch_server(desired_model):
    found_server = []

    for server in server_instances:
        if server.GPU == desired_model:
            found_server.append(server)

    if desired_model == '3090':
        found_server1 = found_server
        
    elif desired_model == 'A800':
        found_server2 = found_server
        
    elif desired_model == 'A100':
        found_server3 = found_server
        
    else:
        found_server4 = found_server
        

    return found_server

def job_and_update(JonLen,JobCOM,queue,process_info):
    
    # for i in tqdm.tqdm(range(JonLen),position=0,leave = True):
    #         time.sleep(JobCOM)
    
    queue.put(process_info)
    shared_pid = os.getpid()
    shared_values.append([shared_pid,shared_progress,process_info])
    for i in range(100):
        q.put(i)
        shared_progress = i
        time.sleep(3)
        #actual delay equals to JobCom


def task(selected_server,path):
    for server in server_instances:
        if selected_server == server.id:
            current_server = server
            break
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    JobCOM = data[0]['complexity_level']
    JonLen = data[0]['length']
    ram = JobCOM*JonLen
    process_info = data[0]
    

    # 若ram不足则需重新分配
    if current_server.availiable_ram < ram:
        return
    
    # 定义临界值 若 可用内存小于此值则认为server不可用
    if current_server.availiable_ram < 0:
        current_server.availiable = False


    current_server.availiable_ram = current_server.availiable_ram - ram
    process = multiprocessing.Process(target=job_and_update,args=(JonLen,JobCOM,queue,process_info))
    process.start()
    process.join()


def instances():
    with open('servers.json', 'r') as json_file:
        server_data = json.load(json_file)
    
    for server_info in server_data:
        server = SubServers(server_info["name"], server_info["ID"], server_info["GPU"], server_info["weight"],24,True)
        server_instances.append(server)



gpus1 = [
    GPU("1", "NV RTX 3008", "1", "2", 10240, 68),
    GPU("2", "NV GTX 1660", "1", "2", 6144, 22),
    GPU("3", "AMD RX 5700 XT", "1", "2", 8192, 40),
]
gpus2 = [
    GPU("1", "NV RTX 3008", "1", "2", 10240, 68),
    GPU("2", "NV GTX 1660", "1", "2", 6144, 22),
    GPU("3", "AMD RX 5700 XT", "1", "2", 8192, 40),
]
# 创建一个拥有多个GPU的资源池
gpu_pool1 = GPUPool(gpus1)

gpu_pool2 = GPUPool(gpus2)

q = multiprocessing.Queue()



# process = multiprocessing.Process(target=worker, args=(q,))
# process.start()

# pbar = tqdm.tqdm(total=100)

# while True:

#         item = q.get(timeout=5)  # 从子进程获取进度信息
#         pbar.update(1)
#         if not process.is_alive():
#             break  # 子进程已经完成，退出循环

# pbar.close()
# process.join()


shared_values = []

def worker(pid):
    shared_pid = os.getpid()
    shared_progress 


shared_progress = multiprocessing.Value('i', 0 ,lock=False)
shared_pid = multiprocessing.Value('i', 0 ,lock=False)
process = multiprocessing.Process(target=worker, args=(q,))
process.start()

pbar = tqdm.tqdm(total=100)


while True:
    if pbar.n == shared_progress:
        time.sleep(2)
        #avoid busy waiting
    pbar.n = shared_progress  # 从子进程获取进度信息
    pbar.last_print_n = shared_progress
    pbar.update(0)
    if not process.is_alive():
        break  # 子进程已经完成，退出循环

pbar.close()
process.join()


def daemon_listener(q):
    logging.basicConfig(filename="jasmine_shell_log.log",
                        level=logging.INFO, format="[%(levelname)s]: %(message)s")

    while True:
        try:
            msg = q.get()
            logging.info(msg)
            if "exit" in msg:
                break
        except Exception as e:
            logging.error(f"Error in listener: {e}")

