from SrdPy.plotGeneric import plotGeneric
from casadi import *
import numpy as np

from SrdPy.InverseKinematics import *

def generateIKTable(IKModelHandler,IKTaskHandler,initialGuess,timeTable,method="lsqnonlin"):
    count = len(timeTable)
    dof = IKModelHandler.dofRobot

    IKTable = np.zeros((count, dof))
    q0 = initialGuess
    for i in range(count):
        if i % np.floor(count / 100) == 0:
            print('Calculating ', str(np.floor(100 * i / count))+ '%')


        t = timeTable[i]
        taskValue = IKTaskHandler.getTask(t)

        solver = None
        
        if method == "lsqnonlin":
            solver = inversePositionProblemSolver_lsqnonlin
        if method == "quadprog":
            solver = inversePositionProblemSolver_quadprog

        q = solver(IKModelHandler.getTask,IKModelHandler.getJacobian,taskValue,q0)
        
        IKTable[i] = q
        q0 = q 

    return IKTable