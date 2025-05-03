#Team members: Urja Chakraborty and Daisy Jiang

#Programming Language Used: Python 

#Brief Description: This program implements a dynamic programming solution for BTSHMULJWNI. Given a list of jobs 
#(each with release time and deadline) and machine types (with capacity and cost), it computes an optimal batch-based schedule with minimum cost,
#as per the definition and constraints in the project description and the referenced research paper. Please feel free to peruse 
#the comments added, for insight into how the program works.

#External Resources Used:
#The provided research paper about Online Flexible Busy Time Scheduling on
#Heterogeneous Machines.

import sys
import os

def read_input_file(filename):
    try:
        with open(filename, 'r') as f:
            # Number of jobs
            n = int(f.readline().strip())
            if n > 1000:
                raise ValueError("The maximum limit of jobs is 1000")
            
            # Each job's release time and deadline
            jobs = []
            for job_id in range(1, n+1):
                r, d = map(int, f.readline().strip().split())
                if d < r:
                    raise ValueError(f"Job {job_id} has deadline before release time")
                jobs.append((r, d, job_id))
            
            # Number of job types
            K = int(f.readline().strip())
            if K > 100:
                raise ValueError("The maximum limit of machine types is 100")
            
            
            # Cost and Capacity
            machines = []
            for _ in range(K):
                c, B = map(int, f.readline().strip().split())
                if c < 1 or B < 1:
                    raise ValueError("The machine cost and capacity must be greater than or equal to 1")
                machines.append((B, c))
        
        return jobs, machines
    # Error handling for the missing file: 
    except FileNotFoundError:
        return None, None
    # General Error Handling
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
        return None, None

def write_output_file(filename, batches):
    with open(filename, 'w') as f:
        # Total number of batches
        f.write(f"{len(batches)}\n") 
        # Batch details including machine type, list of job ids and time
        for batch in batches:
            time, machine_type, job_ids = batch
            job_str = ' '.join(map(str, job_ids))
            f.write(f"{time} {machine_type} {job_str}\n")

# Using dynamic programming to optimize scheduling process
def optimal_schedule(jobs, machines):
    n = len(jobs)
    K = len(machines)
    
    # Sort machines by capacity, then sort by cost
    sort_machines = sorted(machines, key=lambda x: (x[0], x[1]))
    B = [m[0] for m in sort_machines]
    c = [m[1] for m in sort_machines]
    
    # Sort jobs by release time, then sort by deadline from earliest to latest
    sort_jobs = sorted(jobs, key=lambda x: (x[0], x[1]))
    
    A = [float('inf')] * (n + 1) # Stores the minimum cost for scheduling the first q jobs
    A[0] = 0 # Base case: No jobs indicate zero cost
    prev = [-1] * (n + 1)
    batch_info = [None] * (n + 1)
    
    #Consider all batch sizes 1 to min
    for q in range(1, n + 1):
        for l in range(1, min(q, B[-1]) + 1):
            batch_jobs = sort_jobs[q-l:q] # Select the last l jobs
            max_r = max(job[0] for job in batch_jobs) # Find lastest release time 
            min_d = min(job[1] for job in batch_jobs) # Find earliest deadline
            
            # Checks to see if there jobs with the same times
            if max_r > min_d:
                continue
            
            batch_time = max_r  
            # Special handling for batches of size one
            if l == 1:
                job = batch_jobs[0]
                if job[1] == job[0]:  
                    batch_time = job[0]
                else:
                    batch_time = min(job[1], max_r + 1)  
            
            # For each machine type
            for t in range(K):
                if l > B[t]: 
                    continue
                
                # Check if this schedule is optimal and minimizes total cost
                if A[q - l] + c[t] < A[q]:
                    A[q] = A[q - l] + c[t]
                    prev[q] = q - l
                    batch_info[q] = (batch_time, t, l)
    #Reconstruct batch list 
    batches = []
    current = n
    while current > 0:
        time, t, l = batch_info[current]
        job_ids = [sort_jobs[i][2] for i in range(current - l, current)]
        batches.append((time, t, sorted(job_ids)))
        current = prev[current]
    
    batches.sort(key=lambda x: x[0])
    return batches

# Using instance files to produce solution files
def process_files():
    for i in range(1, 100):
        input_file = f"instance{i:02d}.txt"
        output_file = f"solution{i:02d}.txt"
        
        jobs, machines = read_input_file(input_file)
        if jobs is None: 
            continue
            
        batches = optimal_schedule(jobs, machines)
        write_output_file(output_file, batches)
        print(f"Processed {input_file} → {output_file}")

#If script has a specific input filename, process only that file
if __name__ == "__main__":
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        if input_file.startswith("instance") and input_file.endswith(".txt"):
            instance_num = input_file[8:-4]
            output_file = f"solution{instance_num}.txt"
            jobs, machines = read_input_file(input_file)
            if jobs is not None:
                batches = optimal_schedule(jobs, machines)
                write_output_file(output_file, batches)
                print(f"Processed {input_file} → {output_file}")
    # otherwise, process all default files
    else:
        process_files()