# -*- coding: utf-8 -*-
"""Dry and Buy In Furniture manufacturing

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12Bea1I1JBirmloGS7RKABrzI6ACqX17e

HURISTIC METHOD AS PER RESEARCH PAPER
"""

import numpy as np
import random
import time

class KilnScheduler:
    def __init__(self, demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates):
        self.demands = demands
        self.kiln_capacities = kiln_capacities
        self.kiln_availabilities = kiln_availabilities
        self.processing_times = processing_times
        self.buying_costs = buying_costs
        self.drying_costs = drying_costs
        self.due_dates = due_dates
        self.num_jobs = len(demands)
        self.num_kilns = len(kiln_capacities)
        self.schedule = [[] for _ in range(self.num_kilns)]
        self.outsourced = []
        self.cost = 100000
        self.best=[]

    def initial_assignment(self):
        for job in range(self.num_jobs):
            kilns = list(range(self.num_kilns))
            random.shuffle(kilns)  # Randomize kiln ordes
            for kiln in kilns:
                if self.can_assign_job_to_kiln(job, kiln):
                    self.schedule[kiln].append(job)
                    print(self.schedule)
                    break
            else:
                self.outsource_job(job)

    def can_assign_job_to_kiln(self, job, kiln):
        # print(f"trying assignment on kiln : {kiln} present processing time total : {sum(self.processing_times[j][kiln] for j in self.schedule[kiln])+self.kiln_availabilities[kiln]}")
        return (((sum(self.processing_times[j][kiln] for j in self.schedule[kiln])+self.kiln_availabilities[kiln] + self.processing_times[job][kiln]) <= self.due_dates[job]) and (self.demands[job]<=self.kiln_capacities[kiln]))

    def outsource_job(self, job):
        self.outsourced.append(job)

    def improve_schedule(self):
        # This function should implement the heuristic's improvement logic
        # Example: Try exchanging jobs between kilns to reduce total cost or outsourcing

        improved = True
        while(improved):
            improved = False
            for kiln in range(self.num_kilns):
                for job in self.schedule[kiln]:
                    for target_kiln in range(self.num_kilns):
                        if target_kiln != kiln and self.can_exchange_jobs(job, kiln, target_kiln):
                            if(self.calculate_total_cost()<self.cost):
                                self.cost = self.calculate_total_cost()
                                self.best = self.schedule
                                self.schedule[kiln].remove(job)
                                self.schedule[target_kiln].append(job)
                                self.schedule[target_kiln].sort()
                                improved = True
                                break
                    if improved:
                        break
                if improved:
                    break

    def improve_by_swapping(self):
        kiln1 = random.randint(0, len(self.schedule)-1)
        kiln2 = random.randint(0, len(self.schedule)-1)
        while kiln1 == kiln2:
            kiln2 = random.randint(0, len(self.schedule)-1)

        job1 = random.randint(0, len(self.schedule[kiln1])-1)
        job2 = random.randint(0, len(self.schedule[kiln2])-1)

        if self.can_swap(job1, job2, kiln1, kiln2):
            self.swap(job1, job2, kiln1, kiln2)

    def can_swap(self, job1, job2, kiln1, kiln2):
        # Can Fit with demands
        if not self.can_fit_in_kiln(job1, kiln2, sub=self.demands[job2]):
            return False
        elif not self.can_fit_in_kiln(job2, kiln1, sub=self.demands[job1]):
            return False

        # can fit with due dates
        if not self.can_meet_due_date(job1, kiln2, sub=self.processing_times[job2][kiln2]):
            return False
        if not self.can_meet_due_date(job2, kiln1, sub=self.processing_times[job1][kiln1]):
            return False

        return True

    def swap(self, job1, job2, kiln1, kiln2):
        self.schedule[kiln1].remove(job1)
        self.schedule[kiln2].remove(job2)
        self.schedule[kiln1].append(job2)
        self.schedule[kiln2].append(job1)
        self.schedule[kiln1].sort()
        self.schedule[kiln2].sort()

    def add_outsourced(self):
        ans = False
        if len(self.outsourced) > 0:
            job = self.outsourced[0]
            for kiln in range(len(self.schedule)):
                if self.can_fit_in_kiln(job, kiln):
                    ans = True
                    self.outsourced.remove(job)
                    self.schedule[kiln].append(job)
                    self.schedule[kiln].sort()
        return ans



    def can_exchange_jobs(self, job, kiln, target_kiln):
        # Check if moving job to target_kiln violates capacity or due date constraints
        if not self.can_fit_in_kiln(job, target_kiln):
            return False

        # Check if moving job to target_kiln meets its due date constraint
        if not self.can_meet_due_date(job, target_kiln):
            return False

        # Optionally, check if the exchange reduces the total cost
        # This part is simplified; detailed cost comparison logic should be added based on specific needs
        current_cost = self.drying_costs[job][kiln]
        potential_cost = self.drying_costs[job][target_kiln]
        return potential_cost < current_cost

    def can_fit_in_kiln(self, job, kiln, sub=0):
        # Check if the job can fit in the kiln considering the kiln's capacity and other assigned jobs
        return self.demands[job]<=self.kiln_capacities[kiln]

    def can_meet_due_date(self, job, kiln, sub=0):
        # Check if processing the job in the kiln can meet the job's due date
        test = 0
        for j in self.schedule[kiln]:
          test+=self.processing_times[j][kiln]
        processing_end_time = self.kiln_availabilities[kiln] + self.processing_times[job][kiln] + test - sub
        return processing_end_time <= self.due_dates[job]


    def calculate_total_cost(self):
        total_cost = sum(self.buying_costs[job] for job in self.outsourced)
        for kiln, jobs in enumerate(self.schedule):
            for job in jobs:
                total_cost += self.drying_costs[job][kiln]
        return total_cost

    def print_schedule(self):
        for kiln, jobs in enumerate(self.schedule):
            print(f"Kiln {kiln}: Jobs {jobs}")
        print(f"Outsourced Jobs: {self.outsourced}")
        print(f"Total Cost: {self.calculate_total_cost()}")

def generate_random_data(n, num_kilns):
    np.random.seed(0)  # Ensuring reproducibility
    demands = np.random.randint(10, 21, size=n).tolist()
    kiln_capacities = np.random.randint(15, 26, size=num_kilns).tolist()
    kiln_availabilities = np.random.randint(0, 3, size=num_kilns).tolist()
    processing_times = np.random.randint(2, 18, size=(n, num_kilns)).tolist()
    buying_costs = np.random.randint(100, 201, size=n).tolist()
    drying_costs = np.random.randint(20, 56, size=(n, num_kilns)).tolist()
    due_dates = np.sort(np.random.randint(5, 21, size=n)).tolist()
    return demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates

def main():
    n = 100  # Number of jobs
    num_kilns = 10  # Number of kilns

    # Generating random data for the problem
    demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates = generate_random_data(n, num_kilns)
    scheduler = KilnScheduler(demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates)

    scheduler.initial_assignment()
    start_time = time.time()  # Capture start time
    for _ in range(1000):
        scheduler.improve_schedule()
        scheduler.improve_by_swapping()

    scheduler.print_schedule()
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    print(f"Execution Time: {elapsed_time:.2f} seconds")
if __name__ == "__main__":
    main()

import numpy as np
import random
import math
import time

class KilnScheduler:
    def __init__(self, demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates):
        self.demands = demands
        self.kiln_capacities = kiln_capacities
        self.kiln_availabilities = kiln_availabilities
        self.processing_times = processing_times
        self.buying_costs = buying_costs
        self.drying_costs = drying_costs
        self.due_dates = due_dates
        self.num_jobs = len(demands)
        self.num_kilns = len(kiln_capacities)
        self.schedule = [[] for _ in range(self.num_kilns)]
        self.outsourced = []
        self.cost = self.calculate_total_cost()

    def initial_assignment(self):
        for job in range(self.num_jobs):
            kilns = list(range(self.num_kilns))
            random.shuffle(kilns)
            for kiln in kilns:
                if self.can_assign_job_to_kiln(job, kiln):
                    self.schedule[kiln].append(job)
                    break
            else:
                self.outsource_job(job)
        self.cost = self.calculate_total_cost()

    def can_assign_job_to_kiln(self, job, kiln):
        return ((sum(self.processing_times[j][kiln] for j in self.schedule[kiln])+self.kiln_availabilities[kiln] + self.processing_times[job][kiln]) <= self.due_dates[job]) and (self.demands[job] <= self.kiln_capacities[kiln])

    def outsource_job(self, job):
        self.outsourced.append(job)

    def calculate_total_cost(self):
        total_cost = sum(self.buying_costs[job] for job in self.outsourced)
        for kiln, jobs in enumerate(self.schedule):
            for job in jobs:
                total_cost += self.drying_costs[job][kiln]
        return total_cost

    def simulated_annealing(self, start_temp, cooling_rate, min_temp, samples_per_step=5):
        current_temp = start_temp
        self.initial_assignment()
        current_cost = self.cost

        while current_temp > min_temp:
            best_neighbor_cost = float('inf')
            best_neighbor_schedule = None
            best_outsourced = None

            for _ in range(samples_per_step):
                previous_schedule = [list(kiln) for kiln in self.schedule]
                previous_outsourced = list(self.outsourced)

                self.generate_neighbor_solution()
                neighbor_cost = self.calculate_total_cost()

                if neighbor_cost < best_neighbor_cost:
                    best_neighbor_cost = neighbor_cost
                    best_neighbor_schedule = [list(kiln) for kiln in self.schedule]
                    best_outsourced = list(self.outsourced)

                # Revert to previous configuration for the next iteration
                self.schedule = previous_schedule
                self.outsourced = previous_outsourced

            cost_difference = best_neighbor_cost - current_cost
            if cost_difference < 0 or random.random() < math.exp(-cost_difference / current_temp):
                current_cost = best_neighbor_cost
                self.schedule = best_neighbor_schedule
                self.outsourced = best_outsourced

            current_temp *= cooling_rate

        self.cost = current_cost

    def generate_neighbor_solution(self):
        kiln1, kiln2 = np.random.choice(range(self.num_kilns), 2, replace=False)
        if not self.schedule[kiln1] or not self.schedule[kiln2]:
            return

        job1 = random.choice(self.schedule[kiln1])
        job2 = random.choice(self.schedule[kiln2])

        self.schedule[kiln1].remove(job1)
        self.schedule[kiln1].append(job2)
        self.schedule[kiln2].remove(job2)
        self.schedule[kiln2].append(job1)

        if not self.can_assign_job_to_kiln(job2, kiln1) or not self.can_assign_job_to_kiln(job1, kiln2):
            self.schedule[kiln1].remove(job2)
            self.schedule[kiln1].append(job1)
            self.schedule[kiln2].remove(job1)
            self.schedule[kiln2].append(job2)

def generate_random_data(n, num_kilns):
    np.random.seed(0)  # Ensuring reproducibility
    demands = np.random.randint(10, 21, size=n).tolist()
    kiln_capacities = np.random.randint(15, 26, size=num_kilns).tolist()
    kiln_availabilities = np.random.randint(0, 3, size=num_kilns).tolist()
    processing_times = np.random.randint(2, 18, size=(n, num_kilns)).tolist()
    buying_costs = np.random.randint(100, 201, size=n).tolist()
    drying_costs = np.random.randint(20, 56, size=(n, num_kilns)).tolist()
    due_dates = np.sort(np.random.randint(5, 21, size=n)).tolist()
    return demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates

def main():
    n = 100  # Number of jobs
    num_kilns = 10  # Number of kilns

    # Generating random data for the problem
    demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates = generate_random_data(n, num_kilns)

    # Initialize scheduler with random data
    scheduler = KilnScheduler(demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates)

    # Run simulated annealing
    start_time = time.time()
    scheduler.simulated_annealing(start_temp=10000, cooling_rate=0.99, min_temp=1, samples_per_step=5)
    elapsed_time = time.time() - start_time

    # Output results
    print(f"Final Schedule: {scheduler.schedule}")
    print(f"Outsourced Jobs: {scheduler.outsourced}")
    print(f"Final Cost: {scheduler.cost}")
    print(f"Execution Time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()

!pip install pulp

import pulp
import numpy as np
import time

def generate_random_data(n, num_kilns):
    np.random.seed(0)  # For reproducibility
    demands = np.random.randint(10, 21, size=n).tolist()
    kiln_capacities = np.random.randint(20, 31, size=num_kilns).tolist()
    kiln_availabilities = np.random.randint(0, 3, size=num_kilns).tolist()
    processing_times = np.random.randint(1, 10, size=(n, num_kilns)).tolist()
    buying_costs = np.random.randint(100, 201, size=n).tolist()
    drying_costs = np.random.randint(20, 51, size=(n, num_kilns)).tolist()
    due_dates = np.sort(np.random.randint(5, 21, size=n)).tolist()
    return demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates

# Inputs for number of jobs and kilns
n = 100  # Number of jobs
num_kilns = 10  # Number of kilns

# Generate problem data
demands, kiln_capacities, kiln_availabilities, processing_times, buying_costs, drying_costs, due_dates = generate_random_data(n, num_kilns)

# Start measuring time
start_time = time.time()

# Create a PuLP problem instance
problem = pulp.LpProblem("KilnScheduler", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(n) for j in range(num_kilns)), cat=pulp.LpBinary)
o = pulp.LpVariable.dicts("o", (i for i in range(n)), cat=pulp.LpBinary)

# Objective Function: Minimize total cost
problem += pulp.lpSum([drying_costs[i][j] * x[(i, j)] for i in range(n) for j in range(num_kilns)]) + pulp.lpSum([buying_costs[i] * o[i] for i in range(n)])

# Constraints
for i in range(n):
    problem += pulp.lpSum(x[(i, j)] for j in range(num_kilns)) + o[i] == 1, f"Job_{i}_assignment"

for j in range(num_kilns):
    problem += pulp.lpSum(demands[i] * x[(i, j)] for i in range(n)) <= kiln_capacities[j], f"Kiln_{j}_capacity"

for i in range(n):
    for j in range(num_kilns):
        problem += x[(i, j)] * (processing_times[i][j] + kiln_availabilities[j]) <= due_dates[i], f"Due_date_{i}_{j}"

# Solve the problem
problem.solve()

# Calculate execution time
elapsed_time = time.time() - start_time

# Check if a solution is found and display the results
if problem.status == pulp.LpStatusOptimal:
    print("Optimal solution found:\n")
    total_cost = 0
    for i in range(n):
        for j in range(num_kilns):
            if pulp.value(x[(i, j)]) == 1:
                print(f"Job {i} assigned to Kiln {j}.")
                total_cost += drying_costs[i][j]
        if pulp.value(o[i]) == 1:
            print(f"Job {i} outsourced.")
            total_cost += buying_costs[i]
    print(f"Total Cost: {total_cost}")
else:
    print("No optimal solution found.")

# Print execution time
print(f"Execution Time: {elapsed_time:.2f} seconds")
