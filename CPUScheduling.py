import numpy as np
import matplotlib.pyplot as plt
import Processor

speed = 0.1           #Simulation speed. Lower is faster.
numberOfProcesses = 15
arrivalTimeLambda = 15   #for poisson dist. arrivalTime
burstTimeScale = 3.0   #for exponential dist. burstTime
#Initial priorities of the queues
SJFPriority = 0.6    #out of 1 (0.5 = %50)
FCFSPriority = 1 - SJFPriority  #Automatically calculated
maxArrivalTime = 0  #It's set by createPoissonArrivalTimes()
#Creating processes
#list of processes [processID, arrivalTime, burstTime, priority]   priority=1=foreground(SJF), priority=2=batch(FCFS)
#non-preemptive SJF. Other processes must wait.
processPool = []

def createProcessPool():
    print("Creating the process pool...")
    for i in range(numberOfProcesses):
        process = [i+1, 0, 0, np.random.randint(1, 3)]
        processPool.append(process)
    maxArrivalTime = createPoissonArrivalTimes()
    createExponentialBurstTimes()
    print("Process pool succesfully created.")
    return maxArrivalTime

def createPoissonArrivalTimes():
    poisson = np.random.poisson(arrivalTimeLambda, numberOfProcesses) #lambda, size
    for i, arrivalTime in zip(range(numberOfProcesses+1), poisson):
        processPool[i][1] = arrivalTime
    plt.subplot(2, 1, 1)
    plt.hist(poisson)
    plt.tight_layout()
    plt.title('Poisson Arrival Times')
    plt.ylabel('Frequency')
    plt.xlabel('Arrival Times')
    return max(poisson)

def createExponentialBurstTimes():
    exponential = np.random.exponential(burstTimeScale, numberOfProcesses)
    for i, exp in zip(range(numberOfProcesses+1), exponential):
        if int(exp) <= 0:
            burstTime = 1
        else:
            burstTime = int(exp)
        processPool[i][2] = burstTime
    plt.subplot(2, 1, 2)
    plt.hist(exponential)
    plt.tight_layout()
    plt.title('Exponential Burst Times')
    plt.ylabel('Frequency')
    plt.xlabel('Burst Times')

def sortProcessPool():
    def sortByArrivalTime(elem):
        return elem[1]
    processPool.sort(key=sortByArrivalTime)

plt.figure(1)                # the first figure
maxArrivalTime = createProcessPool()
sortProcessPool()   #Sort by arrivalTime

print("Number Of Processes: ", numberOfProcesses)
print("Arrival Time Lambda: ", arrivalTimeLambda)
print("Burst Time Scale: ", burstTimeScale)
print("SJF Priority: ", SJFPriority * 100, "%")
print("FCFS Priority: ", FCFSPriority * 100, "%")
print("[processID, arrivalTime, burstTime, priority]   priority=1=foreground(SJF), priority=2=batch(FCFS)")
print("Process Pool: ", processPool)

Processor.start(SJFPriority, FCFSPriority, processPool, maxArrivalTime, speed)
