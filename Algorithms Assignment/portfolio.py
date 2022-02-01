import csv
from time import time

def loadInvestments(investmentFilename):
    # return a list of possible investment options: name, cost, and estimated return
    # Name = RegionName, cost = Zhvi, estimated return = Zhvi * 10Year (NOTE: Ignore first line United States)
    investList = []
    with open(investmentFilename, 'r') as fin:
        next(fin)
        reader = csv.reader(fin, delimiter=",")
        for row in reader:
            if row[2] != "United States":
                investList.append([row[2], int(row[4]), round(int(row[4])*float(row[9]),2)])

    return investList


def optimizeInvestments(I,A):
    # return optimized profit, how to do that using dynamic programing
    n = len(I)

    # Base case of no investments left or no amount of money left
    if n == 0 or A == 0:
        return 0

    invest = [[None for i in range(A+1)] for j in range(n+1)]
    trace = [[[] for i in range(A+1)] for j in range(n+1)]

    for i in range(A+1):
        invest[0][i] = 0
    for i in range(n+1):
        invest[i][0] = 0

    for i in range(1,n+1):
        for j in range(1,A+1):
            if I[i-1][2] >= 0 and j >= I[i-1][1]:
                remaining = j - int(I[i-1][1])
                if I[i-1][2] + invest[i-1][remaining] > invest[i-1][j]:
                    invest[i][j] = I[i-1][2] + invest[i-1][remaining]
                    if I[i-1][0] not in trace[i][j]:
                        if str(trace[i-1][remaining]) != "[]":
                            win_trace = I[i-1][0] + ", " + str(trace[i-1][remaining])
                        else:
                            win_trace = I[i-1][0]
                        trace[i][j] = win_trace
                else:
                    invest[i][j] = invest[i-1][j]
                    trace[i][j] = trace[i-1][j]
            else:
                invest[i][j] = invest[i-1][j]
                trace[i][j] = trace[i-1][j]

    return invest[n][A], trace[n][A]


t1 = time()
investments = loadInvestments("State_Zhvi_Summary_AllHomes.csv")
investProfit, investList = optimizeInvestments(investments, 1000000)
print("The maximum investment profit is {profit} by making the following home purchases: {states}".format(profit=investProfit,states=investList))
t2 = time()
print(t2-t1)
