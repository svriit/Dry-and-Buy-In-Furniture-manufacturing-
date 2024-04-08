# Kiln Scheduler Optimization

## Overview
The Kiln Scheduler is an optimization tool designed to efficiently allocate kiln resources for various jobs while minimizing costs. It utilizes two primary optimization techniques: Simulated Annealing and Linear Programming via the PuLP library. This tool aims to provide a cost-effective schedule that adheres to job demands, kiln capacities, availability schedules, processing times, and due dates.

## Features
- **Simulated Annealing**: Employs a probabilistic technique for approximating the global optimum of a given function, ideal for navigating the complex scheduling landscape.
- **Linear Programming with PuLP**: Utilizes the PuLP library to solve optimization problems through Linear Programming, providing an alternative, precise method for finding optimal schedules.
- **Customizable Parameters**: Allows for adjustment of job demands, kiln capacities, processing times, and more to fit the specific requirements of various scheduling scenarios.
- **Performance Metrics**: Includes execution time measurement and cost analysis for assessing the efficiency and effectiveness of generated schedules.

## Installation

### Prerequisites
- Python 3.x
- PuLP (`pip install pulp`)
- NumPy (`pip install numpy`)

### Setup
Clone the repository to your local machine:

