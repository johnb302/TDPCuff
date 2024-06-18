import multiprocessing as mp

ard_processes = []

def set_processes(process_list):
    global ard_processes
    ard_processes = process_list

def terminate_processes():
    global ard_processes
    for process in ard_processes:
        process.terminate()