import sys
import os

def read_input(filename):
    try:
        with open(filename, 'r') as f:
            n = int(f.readline().strip())
            if n > 1000:
                raise ValueError("Number of jobs exceeds maximum limit of 1000")
                
            jobs = []
            for job_id in range(1, n+1):
                r, d = map(int, f.readline().strip().split())
                if d < r:
                    raise ValueError(f"Job {job_id} has deadline before release time")
                jobs.append((r, d, job_id))
            
            K = int(f.readline().strip())
            if K > 100:
                raise ValueError("Number of machine types exceeds maximum limit of 100")
                
            machines = []
            for _ in range(K):
                c, B = map(int, f.readline().strip().split())
                if c < 1 or B < 1:
                    raise ValueError("Machine cost and capacity must be ≥ 1")
                machines.append((B, c))
        
        return jobs, machines
    except FileNotFoundError:
        return None, None
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
        return None, None

def write_output(filename, batches):
    with open(filename, 'w') as f:
        f.write(f"{len(batches)}\n")
        for batch in batches:
            time, machine_type, job_ids = batch
            job_str = ' '.join(map(str, job_ids))
            f.write(f"{time} {machine_type} {job_str}\n")

def get_optimal_schedule(jobs, machines):
    n = len(jobs)
    K = len(machines)
    
    machines_sorted = sorted(machines, key=lambda x: (x[0], x[1]))
    B = [m[0] for m in machines_sorted]
    c = [m[1] for m in machines_sorted]
    
    jobs_sorted = sorted(jobs, key=lambda x: (x[0], x[1]))
    
    A = [float('inf')] * (n + 1)
    A[0] = 0
    prev = [-1] * (n + 1)
    batch_info = [None] * (n + 1)
    
    for q in range(1, n + 1):
        for l in range(1, min(q, B[-1]) + 1):
            batch_jobs = jobs_sorted[q-l:q]
            max_r = max(job[0] for job in batch_jobs)
            min_d = min(job[1] for job in batch_jobs)
            
            if max_r > min_d:
                continue
            
            batch_time = max_r  
            
            if l == 1:
                job = batch_jobs[0]
                if job[1] == job[0]:  
                    batch_time = job[0]
                else:
                    batch_time = min(job[1], max_r + 1)  
            
            for t in range(K):
                if l > B[t]:
                    continue
                
                if A[q - l] + c[t] < A[q]:
                    A[q] = A[q - l] + c[t]
                    prev[q] = q - l
                    batch_info[q] = (batch_time, t, l)
    
    batches = []
    current = n
    while current > 0:
        time, t, l = batch_info[current]
        job_ids = [jobs_sorted[i][2] for i in range(current - l, current)]
        batches.append((time, t, sorted(job_ids)))
        current = prev[current]
    
    batches.sort(key=lambda x: x[0])
    return batches

def process_files():
    for i in range(1, 100):
        input_file = f"instance{i:02d}.txt"
        output_file = f"solution{i:02d}.txt"
        
        jobs, machines = read_input(input_file)
        if jobs is None: 
            continue
            
        batches = get_optimal_schedule(jobs, machines)
        write_output(output_file, batches)
        print(f"Processed {input_file} → {output_file}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        if input_file.startswith("instance") and input_file.endswith(".txt"):
            instance_num = input_file[8:-4]
            output_file = f"solution{instance_num}.txt"
            jobs, machines = read_input(input_file)
            if jobs is not None:
                batches = get_optimal_schedule(jobs, machines)
                write_output(output_file, batches)
                print(f"Processed {input_file} → {output_file}")
    else:
        process_files()