import time
import numpy as np
import sys
import matplotlib.pyplot as plt
from queue import Queue

def start(SJFPriority, FCFSPriority, processPool, maxArrivalTime, speed):
    masterClock = 0  #InitialValue
    isBusy = False
    checkIndex = 0 #The process which is being checked from the process pool
    nextArrivalTime = processPool[checkIndex][1]
    processPoolLength = len(processPool)
    SJFQueue = []
    FCFSQueue = Queue()
    SJFTurnaroundTimes = []
    SJFAverageTurnaroundTime = 0
    FCFSTurnaroundTimes = []
    FCFSAverageTurnaroundTime = 0
    SJFWaitingTimes = []
    SJFAverageWaitingTime = 0
    FCFSWaitingTimes = []
    FCFSAverageWaitingTime = 0
    SJFQueueLengths = []
    SJFAverageQueueLength = 0
    FCFSQueueLengths = []
    FCFSAverageQueueLength = 0
    timeSpentForProcesses = 0; CPUUtilization = 0; CPUUtilizationData = []   #For CPU utilization calculation
    numberOfTerminatedProcesses = 0; throughput = 0; throughputData = []; masterClockData = [] #For throughput calculation
    SJFAverageQueueLengths = []; FCFSAverageQueueLengths = []  #For plotting average queue lengths
    SJFAverageTurnaroundTimes = []; FCFSAverageTurnaroundTimes = []  #For plotting average turnaround times
    SJFPriorityData = []; FCFSPriorityData = []  #For plotting priority chart
    SJFAverageWaitingTimes = []; FCFSAverageWaitingTimes = []  #For plotting average waiting times
    #Temporary process info which is being processed; [processID, arrivalTime, remainingBurstTime, priority]
    processInfo = [None, None, None, None]
    recentIdle = 0  #It holds recent idle clock. It is used to prevent prioritizing over and over

    def placeToQueues(checkIndex, nextArrivalTime):
        def isNextProcessSameTime(checkIndex, nextArrivalTime):
            if checkIndex + 1 < processPoolLength:
                if processPool[checkIndex+1][1] == processPool[checkIndex][1]:
                    checkIndex += 1
                    checkIndex, nextArrivalTime = placeToQueues(checkIndex, nextArrivalTime)
                    return checkIndex, nextArrivalTime
                else:
                    checkIndex += 1
                    nextArrivalTime = processPool[checkIndex][1]
                    return checkIndex, nextArrivalTime
            else:
                return checkIndex, nextArrivalTime

        if processPool[checkIndex][3] == 1:      #SJF priority process
            SJFQueue.append(processPool[checkIndex])
            SJFQueue.sort(key=sortByBurstTime)
            return isNextProcessSameTime(checkIndex, nextArrivalTime)

        elif processPool[checkIndex][3] == 2:    #FCFS priority process
            FCFSQueue.put(processPool[checkIndex])
            return isNextProcessSameTime(checkIndex, nextArrivalTime)
        else:
            sys.exit("Invalid queue priority")

    def chooseFromQueues():
        print(" Choosing from queues algorithm is working...")
        if len(SJFQueue) > 0 and not FCFSQueue.empty():     #if both queues are not empty
            choice = round(np.random.random(), 1)
            if choice < SJFPriority:
                 #SJF is chosen
                 print(" Both of the queues have at least one process and SJF Queue was chosen.")
                 processInfo = SJFQueue.pop(0)   #Pop the first element(it's already sorted by shortest job).
            else:
                #FCFS is chosen
                print(" Both of the queues have at least one process and FCFS Queue was chosen.")
                processInfo = FCFSQueue.get()  #Take the first element from the queue. (First comes first served)
        else:
            if len(SJFQueue) > 0:
                #SJF
                print(" Only the SJF Queue has at least one process.")
                processInfo = SJFQueue.pop(0)   #Pop the first element(it's already sorted by shortest job).
            elif not FCFSQueue.empty():
                #FCFS
                print("  Only the FCFS Queue has at least one process.")
                processInfo = FCFSQueue.get()   #Take the first element from the queue.
        print(" processInfo: ", processInfo)
        return processInfo

    print("Processor is running...")
    while (isBusy == True) or (masterClock <= maxArrivalTime) or (len(SJFQueue) > 0 or not FCFSQueue.empty()): #masterClock loop
        if masterClock > 0:           #Zero division handling
            CPUUtilization = timeSpentForProcesses / masterClock
            throughput = numberOfTerminatedProcesses / masterClock
            CPUUtilizationData.append(round(CPUUtilization*100, 2))
            throughputData.append(round(throughput, 2))
            masterClockData.append(masterClock)
            #Calculate average queue lengths for plotting
            SJFAverageQueueLengths.append(sum(SJFQueueLengths) / len(SJFQueueLengths))
            FCFSAverageQueueLengths.append(sum(FCFSQueueLengths) / len(FCFSQueueLengths))
            #Calculate average turnaround times for plotting
            if len(SJFTurnaroundTimes) < 1:  #Zero division handling
                SJFAverageTurnaroundTimes.append(0)
            else:
                SJFAverageTurnaroundTimes.append(sum(SJFTurnaroundTimes) / len(SJFTurnaroundTimes))
            if len(FCFSTurnaroundTimes) < 1:  #Zero division handling
                FCFSAverageTurnaroundTimes.append(0)
            else:
                FCFSAverageTurnaroundTimes.append(sum(FCFSTurnaroundTimes) / len(FCFSTurnaroundTimes))
            #Calculate average waiting times for plotting
            if len(SJFWaitingTimes) < 1:  #Zero division handling
                SJFAverageWaitingTimes.append(0)
            else:
                SJFAverageWaitingTimes.append(sum(SJFWaitingTimes) / len(SJFWaitingTimes))
            if len(FCFSWaitingTimes) < 1:  #Zero division handling
                FCFSAverageWaitingTimes.append(0)
            else:
                FCFSAverageWaitingTimes.append(sum(FCFSWaitingTimes) / len(FCFSWaitingTimes))

        print("---------------masterClock:", masterClock)
        #Calculate queue lengths
        SJFQueueLengths.append(len(SJFQueue))
        FCFSQueueLengths.append(FCFSQueue.qsize())

        if nextArrivalTime == masterClock:   #is there any process which its arrivalTime is equal to the masterClock
            print(" At least one arrivalTime which is equal to the masterClock has found. Placing to the queues...")
            checkIndex, nextArrivalTime = placeToQueues(checkIndex, nextArrivalTime)
        if isBusy == True:
            print(" Processor is now busy.")
            processInfo[2] -= 1     #decrease remainingBurstTime
            if (processInfo[2]) == 0:  #is process finished
                isBusy = False            #Process terminated
                numberOfTerminatedProcesses += 1
                print("", processInfo[0], "ID numbered process terminated.")
                #Calculate turnaround times
                if processInfo[3] == 1:        #SJF queue process
                    SJFTurnaroundTimes.append(masterClock - processInfo[1])  #MC-arrivalTime
                else:                         #FCFS queue process
                    FCFSTurnaroundTimes.append(masterClock - processInfo[1]) #MC-arrivalTime
                processInfo = [None, None, None, None]
            else:
                timeSpentForProcesses += 1   #For CPU utilization calculation
                #Calculate waiting times
                if processInfo[3] == 1:        #SJF queue process
                    SJFWaitingTimes.append(masterClock - processInfo[1])  #MC-arrivalTime
                else:                         #FCFS queue process
                    FCFSWaitingTimes.append(masterClock - processInfo[1]) #MC-arrivalTime
        if isBusy == False:
            print(" Checking the queues hence the processor is not busy...")
            if len(SJFQueue) > 0 or not FCFSQueue.empty():     #if there is any unprocessed process in the queues
                print(" There is at least one process in the queues.")
                processInfo = chooseFromQueues()
                #Calculate waiting times
                if processInfo[3] == 1:        #SJF queue process
                    SJFWaitingTimes.append(masterClock - processInfo[1])  #MC-arrivalTime
                else:                         #FCFS queue process
                    FCFSWaitingTimes.append(masterClock - processInfo[1]) #MC-arrivalTime
                #Execute the process
                print(" A new process is being started...")
                isBusy = True
            else:
                print(" Both of the queues are empty")

        print(" masterClock: {}\n isBusy: {}\n WorkingProcessID: {}\n remainingBurstTime: {}\n SJFPriority: {}%\n FCFSPriority: {}%\n SJFQueueLen: {}\n FCFSQueueLen: {}" .format(masterClock, isBusy, processInfo[0], processInfo[2], round(SJFPriority*100, 2), round(FCFSPriority*100, 2), len(SJFQueue), FCFSQueue.qsize()))

        if isBusy == False and not (len(SJFQueue) > 0 or not FCFSQueue.empty()):  #Idle state: processor is not busy and queues are empty, balance queue priority
            print(" The processor is not busy and both of the queues are empty. (Idle State)**********")
            #Calculate ATT, AWT, AQL and balance the queue priority
            if masterClock > 0:           #Zero division handling
                CPUUtilization = timeSpentForProcesses / masterClock
                throughput = numberOfTerminatedProcesses / masterClock
            print(" CPU Utilization:", round(CPUUtilization*100, 2), "%")
            print(" Throughput:", round(throughput, 2))
            if len(SJFTurnaroundTimes) > 0:           #Zero division handling
                SJFAverageTurnaroundTime = sum(SJFTurnaroundTimes) / len(SJFTurnaroundTimes)
            print(" SJFAverageTurnaroundTime:", round(SJFAverageTurnaroundTime, 2))
            if len(FCFSTurnaroundTimes) > 0:           #Zero division handling
                FCFSAverageTurnaroundTime = sum(FCFSTurnaroundTimes) / len(FCFSTurnaroundTimes)
            print(" FCFSAverageTurnaroundTime:", round(FCFSAverageTurnaroundTime, 2))
            if len(SJFWaitingTimes) > 0:           #Zero division handling
                SJFAverageWaitingTime = sum(SJFWaitingTimes) / len(SJFWaitingTimes)
            print(" SJFAverageWaitingTime:", round(SJFAverageWaitingTime, 2))
            if len(FCFSWaitingTimes) > 0:           #Zero division handling
                FCFSAverageWaitingTime = sum(FCFSWaitingTimes) / len(FCFSWaitingTimes)
            print(" FCFSAverageWaitingTime:", round(SJFAverageWaitingTime, 2))
            if len(SJFQueueLengths) > 0:           #Zero division handling
                SJFAverageQueueLength = sum(SJFQueueLengths) / len(SJFQueueLengths)
            print(" SJFAverageQueueLength:", round(SJFAverageQueueLength, 2))
            if len(FCFSQueueLengths) > 0:           #Zero division handling
                FCFSAverageQueueLength = sum(FCFSQueueLengths) / len(FCFSQueueLengths)
            print(" FCFSAverageQueueLength:", round(FCFSAverageQueueLength, 2))

            if len(SJFTurnaroundTimes) > 0 and len(FCFSTurnaroundTimes) > 0:  #If both queues were used once, recalculate priorities
                SJFQueueStatus = (SJFAverageTurnaroundTime + SJFAverageWaitingTime + SJFAverageQueueLength) / 3
                FCFSQueueStatus = (FCFSAverageTurnaroundTime + FCFSAverageWaitingTime + FCFSAverageQueueLength) / 3
                print(" Evaluating the queue priorities... (Higher value should be prioritized.)")
                print(" SJFQueueStatus: ", round(SJFQueueStatus, 2))
                print(" FCFSQueueStatus: ", round(FCFSQueueStatus, 2))

                if not recentIdle == masterClock - 1:       #To avoid increasing priority over and over
                    if FCFSQueueStatus > SJFQueueStatus:     #If FCFS queue's values are worse, give more priority to FCFS queue
                        print(" Prioritizing the FCFS Queue...")
                        if round(FCFSPriority, 1) < 0.9:    #Check if its priority is maximum
                            FCFSPriority += 0.1        #Give 10% more priority
                            SJFPriority = 1 - FCFSPriority
                        else:
                            print(" FCFS Queue has already reached maximum priority.")
                        print(" SJFPriority: ", round(SJFPriority*100, 2), "% FCFSPriority: ", round(FCFSPriority*100, 2), "% priorities balanced.")
                    elif SJFQueueStatus > FCFSQueueStatus:  #If SJF queue's values are worse, give more priority to SJF queue
                        print(" Prioritizing the SJF Queue...")
                        if round(SJFPriority, 1) < 0.9:  #Check if its priority is maximum
                            SJFPriority += 0.1          #Give 10% more priority
                            FCFSPriority = 1 - SJFPriority
                        else:
                            print(" SJF Queue has already reached maximum priority.")
                        print(" SJFPriority: ", round(SJFPriority*100, 2), "% FCFSPriority: ", round(FCFSPriority*100, 2), "% priorities balanced.")
            recentIdle = masterClock


        SJFPriorityData.append(round(SJFPriority*100, 2))
        FCFSPriorityData.append(round(FCFSPriority*100, 2))
        time.sleep(speed)  #Delay for the simulation speed
        masterClock += 1

    plt.figure(2)                # the second figure
    plt.subplot(2, 2, 1)
    plt.plot(masterClockData, CPUUtilizationData)
    plt.grid()
    plt.fill_between(masterClockData, 0, CPUUtilizationData, alpha='0.4')
    plt.tight_layout()
    plt.title('CPU Utilization (%)')
    plt.ylabel('CPU Utilization (%)')
    plt.xlabel('Master Clock')

    plt.subplot(2, 2, 3)
    plt.plot(masterClockData, throughputData, color='purple')
    plt.grid()
    plt.fill_between(masterClockData, 0, throughputData, color='purple', alpha='0.4')
    plt.tight_layout()
    plt.title('Throughput')
    plt.xlabel('Master Clock')
    plt.ylabel('Throughput')

    plt.subplot(2, 2, 2)
    ind = np.arange(masterClock)
    width = 0.70
    p1 = plt.bar(ind, SJFQueueLengths, width, color = 'red')
    p2 = plt.bar(ind, FCFSQueueLengths, width, bottom=SJFQueueLengths, color = 'green')
    plt.grid()
    plt.tight_layout()
    plt.title('Queue Lengths')
    plt.ylabel('Lengths')
    plt.xlabel('Master Clock')
    plt.legend((p1[0], p2[0]), ('SJFQueue', 'FCFSQueue'))

    plt.subplot(2, 2, 4)
    ind = np.arange(masterClock)
    width = 0.70
    p1 = plt.bar(ind, SJFPriorityData, width, color = 'red')
    p2 = plt.bar(ind, FCFSPriorityData, width, bottom=SJFPriorityData, color = 'green')
    plt.grid()
    plt.tight_layout()
    plt.title('Queue Priorities (%)')
    plt.ylabel('Priority Values (%)')
    plt.xlabel('Master Clock')
    plt.legend((p1[0], p2[0]), ('SJFPriority', 'FCFSPriority'))

    plt.figure(3)                # the third figure
    plt.subplot(2, 2, 1)
    plt.plot(masterClockData, SJFAverageQueueLengths, color = 'red', label = 'SJFAQL')
    plt.plot(masterClockData, FCFSAverageQueueLengths, color = 'green', label = 'FCFSAQL')
    plt.grid()
    plt.tight_layout()
    plt.title('Average Queue Lengths')
    plt.ylabel('Average Queue Length')
    plt.xlabel('Master Clock')
    plt.legend()


    plt.subplot(2, 2, 3)
    plt.plot(FCFSPriorityData, SJFPriorityData, marker = 'o', color = 'purple')
    #Rotating the graph according to time
    plt.ylim(min(SJFPriorityData)-1, max(SJFPriorityData)+1)
    if FCFSPriorityData[-1] < SJFPriorityData[-1]:
        plt.xlim(max(FCFSPriorityData)+1, min(FCFSPriorityData)-1)
    else:
        plt.xlim(min(FCFSPriorityData)-1, max(FCFSPriorityData)+1)
    plt.grid()
    plt.tight_layout()
    plt.title('Priority to Priority Chart')
    plt.ylabel('SJF Queue Priority')
    plt.xlabel('FCFS Queue Priority')

    plt.subplot(2, 2, 2)
    plt.plot(masterClockData, SJFAverageTurnaroundTimes, color = 'red', label = 'SJFATT')
    plt.plot(masterClockData, FCFSAverageTurnaroundTimes, color = 'green', label = 'FCFSATT')
    plt.grid()
    plt.tight_layout()
    plt.title('Average Turnaround Times')
    plt.ylabel('Average Turnaround Time')
    plt.xlabel('Master Clock')
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(masterClockData, SJFAverageWaitingTimes, color = 'red', label = 'SJFAWT')
    plt.plot(masterClockData, FCFSAverageWaitingTimes, color = 'green', label = 'FCFSAWT')
    plt.grid()
    plt.tight_layout()
    plt.title('Average Waiting Times')
    plt.ylabel('Average Waiting Time')
    plt.xlabel('Master Clock')
    plt.legend()

    plt.figure(4)                # the fourth figure
    plt.subplot(2, 1, 1)
    ind = np.arange(len(SJFTurnaroundTimes))
    ind2 = np.arange(len(FCFSTurnaroundTimes))
    plt.plot(ind, SJFTurnaroundTimes, color = 'red', label = 'SJFTT')
    plt.plot(ind2, FCFSTurnaroundTimes, color = 'green', label = 'FCFSTT')
    plt.grid()
    plt.tight_layout()
    plt.title('Turnaround Times')
    plt.ylabel('Turnaround Time')
    plt.xlabel('Processed Processes')
    plt.legend()

    plt.subplot(2, 1, 2)
    ind = np.arange(len(SJFWaitingTimes))
    ind2 = np.arange(len(FCFSWaitingTimes))
    plt.plot(ind, SJFWaitingTimes, color = 'red', label = 'SJFWT')
    plt.plot(ind2, FCFSWaitingTimes, color = 'green', label = 'FCFSWT')
    plt.grid()
    plt.tight_layout()
    plt.title('Waiting Times')
    plt.ylabel('Waiting Time')
    plt.xlabel('Calculating Number')
    plt.legend()

    plt.show()


def sortByBurstTime(elem):
    return elem[2]
