ard_instances = []

def set_instances(instance_list):
    global ard_instances
    ard_instances = instance_list

def terminate_processes():
    global ard_instances
    
    for arduino in ard_instances:
        arduino.stop()
