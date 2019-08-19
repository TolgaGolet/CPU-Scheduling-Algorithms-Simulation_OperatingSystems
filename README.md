# CPU-Scheduling-Algorithms-Simulation_OperatingSystems
Multilevel Dynamic Priority Queue CPU Scheduling Algorithm Simulation

# Project Description

This project aims to simulate a CPU scheduling algorithm which is a multilevel dynamic priority queue. There are 2 queues implemented in this project. First queue is the Shortest Job First algorithm queue which works in non-preemptive way and the second one is a First Come First Served algorithm queue. The priority indices of the queues are dynamically set by CPU at idle times. At each idle time, CPU calculates average turnaround times, average queue lengths, average waiting times and sets the priority indices by evaluating those values. For example if there is a queue which its waiting time is too high so the evaluating value is too high, the CPU automatically increases corresponding queues priority by 10%. In this project, arrival times of the processes are generated with Poisson distribution and burst times of the processes are generated with exponential distribution.

# Screenshots

![screenshot](https://github.com/TolgaGolet/CPU-Scheduling-Algorithms-Simulation_OperatingSystems/blob/master/Screenshots/Screenshot.png)
![screenshot](https://github.com/TolgaGolet/CPU-Scheduling-Algorithms-Simulation_OperatingSystems/blob/master/Screenshots/Screenshot2.png)
![screenshot](https://github.com/TolgaGolet/CPU-Scheduling-Algorithms-Simulation_OperatingSystems/blob/master/Screenshots/Screenshot3.png)
![screenshot](https://github.com/TolgaGolet/CPU-Scheduling-Algorithms-Simulation_OperatingSystems/blob/master/Screenshots/Screenshot4.png)
![screenshot](https://github.com/TolgaGolet/CPU-Scheduling-Algorithms-Simulation_OperatingSystems/blob/master/Screenshots/Screenshot5.png)
![screenshot](https://github.com/TolgaGolet/CPU-Scheduling-Algorithms-Simulation_OperatingSystems/blob/master/Screenshots/Screenshot6.png)
![screenshot](https://github.com/TolgaGolet/CPU-Scheduling-Algorithms-Simulation_OperatingSystems/blob/master/Screenshots/Screenshot7.png)

# Requirements

Matplotlib <br/>
Numpy
