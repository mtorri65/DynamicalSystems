import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


def eigenvalues(x, y, mu, delta):
    discriminant = delta**2 - 4*mu
    Re_lambda1 = 0
    Re_lambda2 = 0
    Im_lambda1 = 0
    Im_lambda2 = 0
    if discriminant >= 0:
        Re_lambda1 = -delta/2 - np.sqrt(discriminant)/2
        Re_lambda2 = -delta/2 + np.sqrt(discriminant)/2
        Im_lambda1 = 0
        Im_lambda2 = 0
    else:
        Re_lambda1 = -delta/2 
        Re_lambda2 = -delta/2 
        Im_lambda1 = -np.sqrt(-discriminant)/2
        Im_lambda2 = np.sqrt(-discriminant)/2
    return Re_lambda1, Re_lambda2, Im_lambda1, Im_lambda2

meshLines = 100
textHorizontalPosition = 0.0

class genericExercise(ABC):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSideLength, textVerticalPosition) -> None:
        self.numPlotsPerColumn = numPlotsPerColumn
        self.numPlotsPerRow = numPlotsPerRow
        self.figHorizontalSize = figHorizontalSize
        self.figVerticalSize = figVerticalSize
        self.fig = plt.figure
        self.axes = plt.axes
        self.plotSideLength = plotSideLength
        self.textVerticalPosition = textVerticalPosition
        self.X = []
        self.Y = []
        self.parameters = []

    def configurePlot(self):
        self.X, self.Y = np.meshgrid(np.linspace(-self.plotSideLength, self.plotSideLength, meshLines), np.linspace(-self.plotSideLength, self.plotSideLength, meshLines))
        self.R = np.sqrt(self.X**2 + self.Y**2)
        self.THETA = np.arctan2(self.X, self.Y) 
        self.fig, self.axes = plt.subplots(self.numPlotsPerColumn, self.numPlotsPerRow, figsize=(self.figHorizontalSize, self.figVerticalSize))

    @abstractmethod
    def parameterCases(self):
        pass

    @abstractmethod
    def calculatePhasePortrait(self, x, y, delta, mu):
        pass

    @abstractmethod
    def drawPhasePortrait(self, title):
        pass

class Exercise1(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':-1.0, 'delta':-1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':2.0, 'delta':-4.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':5.0, 'delta':-4.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, x, y, delta, mu):        
        return y, -delta*y - mu*x
    
    def drawPhasePortrait(self, title):
        self.configurePlot()
        self.parameterCases()
        for row in range(2):
            for caseNumber in range(len(self.parameters)):
                mu = self.parameters[caseNumber]['mu'] 
                delta = self.parameters[caseNumber]['delta']
                if row > 0:
                    delta = -delta 
                plotTitle = '(' + str(row*self.numPlotsPerRow + caseNumber + 1) + ') mu = ' + str(mu) + ', delta = ' + str(delta)
                ax = self.axes[row][caseNumber]
                dX, dY = self.calculatePhasePortrait(self.X, self.Y, delta, mu)
                speed = np.sqrt(dX**2 + dY**2)
                lw = 3*speed / speed.max()
                ax.streamplot(self.X, self.Y, dX, dY, color='r', linewidth=lw, density=0.8)
#                self.fig.suptitle('Problem 1.6.1 - Non Degenerate Cases', fontsize=20)
                self.fig.suptitle(title, fontsize=20)
                ax.text(textHorizontalPosition, self.textVerticalPosition, plotTitle, horizontalalignment='center',
                        fontsize=10, bbox=dict(facecolor='white', edgecolor='none'))
        plt.show()

class Exercise2(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':1.0, 'delta':2.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':0.0, 'delta':-1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':-1.0, 'delta':0.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':0.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, x, y, delta, mu):
        return y, -delta*y - mu*x
    
    def drawPhasePortrait(self, title):
        self.configurePlot()
        self.parameterCases()
        for row in range(2):
            for caseNumber in range(len(self.parameters)):
                mu = self.parameters[caseNumber]['mu'] 
                delta = self.parameters[caseNumber]['delta']
                if row > 0:
                    delta = -delta 
                plotTitle = '(' + str(row*self.numPlotsPerRow + caseNumber + 1) + ') mu = ' + str(mu) + ', delta = ' + str(delta)
                ax = self.axes[row][caseNumber]
                dX, dY = self.calculatePhasePortrait(self.X, self.Y, delta, mu)
                speed = np.sqrt(dX**2 + dY**2)
                lw = 3*speed / speed.max()
                ax.streamplot(self.X, self.Y, dX, dY, color='r', linewidth=lw, density=0.8)
#                self.fig.suptitle('Problem 1.6.1 - Degenerate Cases', fontsize=20)
                self.fig.suptitle(title, fontsize=20)
                ax.text(textHorizontalPosition, self.textVerticalPosition, plotTitle, horizontalalignment='center',
                        fontsize=10, bbox=dict(facecolor='white', edgecolor='none'))
        plt.show()

class Exercise3(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':1.0, 'delta':2.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':0.0, 'delta':-1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':-1.0, 'delta':0.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, x, y, delta, mu):
        return -x + x**3, x + y
    
    def drawPhasePortrait(self, title):
        self.configurePlot()
        self.parameterCases()
        for row in range(2):
            for caseNumber in range(len(self.parameters)):
                mu = self.parameters[caseNumber]['mu'] 
                delta = self.parameters[caseNumber]['delta']
                if row > 0:
                    delta = -delta 
                plotTitle = '(' + str(row*self.numPlotsPerRow + caseNumber + 1) + ') mu = ' + str(mu) + ', delta = ' + str(delta)
                ax = self.axes[row][caseNumber]
                dX, dY = self.calculatePhasePortrait(self.X, self.Y, delta, mu)
                speed = np.sqrt(dX**2 + dY**2)
                lw = 3*speed / speed.max()
                ax.streamplot(self.X, self.Y, dX, dY, color='r', linewidth=lw, density=0.8)
#                self.fig.suptitle('Problem 1.6.1 - Degenerate Cases', fontsize=20)
                self.fig.suptitle(title, fontsize=20)
                ax.text(textHorizontalPosition, self.textVerticalPosition, plotTitle, horizontalalignment='center',
                        fontsize=10, bbox=dict(facecolor='white', edgecolor='none'))
        plt.show()


class Exercise4(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, x, y, delta, mu):
        return -delta*x - mu*y + x*y, mu*x - delta*y + 0.5*(x**2 - y**2)
    
    def drawPhasePortrait(self, title):
        self.configurePlot()
        self.parameterCases()
        for row in range(2):
            for caseNumber in range(len(self.parameters)):
                mu = self.parameters[caseNumber]['mu'] 
                delta = self.parameters[caseNumber]['delta']
                if row > 0:
                    delta = -delta 
                plotTitle = '(' + str(row*self.numPlotsPerRow + caseNumber + 1) + ') mu = ' + str(mu) + ', delta = ' + str(delta)
                ax = self.axes[row][caseNumber]
                Xdot, Ydot = self.calculatePhasePortrait(self.X, self.Y, delta, mu)
                speed = np.sqrt(Xdot**2 + Ydot**2)
                lw = 3*speed / speed.max()
                ax.streamplot(self.X, self.Y, Xdot, Ydot, color='r', linewidth=lw, density=0.8)
#                self.fig.suptitle('Problem 1.6.1 - Degenerate Cases', fontsize=20)
                self.fig.suptitle(title, fontsize=20)
                ax.text(textHorizontalPosition, self.textVerticalPosition, plotTitle, horizontalalignment='center',
                        fontsize=10, bbox=dict(facecolor='white', edgecolor='none'))
        plt.show()

class Exercise5(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, r, theta, delta, mu):
        return r*(1 - r**2), np.cos(4*theta)
    
    def drawPhasePortrait(self, title):
        self.configurePlot()
        self.parameterCases()
        for row in range(2):
            for caseNumber in range(len(self.parameters)):
                mu = self.parameters[caseNumber]['mu'] 
                delta = self.parameters[caseNumber]['delta']
                if row > 0:
                    delta = -delta 
                plotTitle = '(' + str(row*self.numPlotsPerRow + caseNumber + 1) + ') mu = ' + str(mu) + ', delta = ' + str(delta)
                ax = self.axes[row][caseNumber]
                Rdot, THETAdot = self.calculatePhasePortrait(self.R, self.THETA, delta, mu)
                speed = np.sqrt(Rdot**2 + self.R**2*THETAdot**2)
                lw = 3*speed / speed.max()
                ax.streamplot(self.X, self.Y, Rdot, self.R*THETAdot, color='r', linewidth=lw, density=0.8)
#                self.fig.suptitle('Problem 1.6.1 - Degenerate Cases', fontsize=20)
                self.fig.suptitle(title, fontsize=20)
                ax.text(textHorizontalPosition, self.textVerticalPosition, plotTitle, horizontalalignment='center',
                        fontsize=10, bbox=dict(facecolor='white', edgecolor='none'))
        plt.show()

class Example7(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, x, y, delta, mu):
        return x, x**2 + y**2 - 1
    
    def drawPhasePortrait(self, title):
        super().drawPhasePortrait(self, title)

    def drawPhasePortraitNoParameters(self, title):
        self.configurePlot()
        dX, dY = self.calculatePhasePortrait(self.X, self.Y, 0, 0)
        speed = np.sqrt(dX**2 + dY**2)
        lw = 5*speed / speed.max()
        plt.streamplot(self.X, self.Y, dX, dY, color='r', linewidth=lw, density=2.0)
        plt.show()

class Example8(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, x, y, delta, mu):
        return y, x*(1 - x**2) + y
    
    def drawPhasePortrait(self, title):
        super().drawPhasePortrait(self, title)

    def drawPhasePortraitNoParameters(self, title):
        self.configurePlot()
        dX, dY = self.calculatePhasePortrait(self.X, self.Y, 0, 0)
        speed = np.sqrt(dX**2 + dY**2)
        lw = 5*speed / speed.max()
        plt.streamplot(self.X, self.Y, dX, dY, color='r', linewidth=lw, density=2.0)
        plt.show()

class Example9(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, x, y, delta, mu):
        return x*(1 - x/2 - y), y*(x - 1 - y/2)
    
    def drawPhasePortrait(self, title):
        super().drawPhasePortrait(self, title)

    def drawPhasePortraitNoParameters(self, title):
        self.configurePlot()
        dX, dY = self.calculatePhasePortrait(self.X, self.Y, 0, 0)
        speed = np.sqrt(dX**2 + dY**2)
        lw = 5*speed / speed.max()
        plt.streamplot(self.X, self.Y, dX, dY, color='r', linewidth=lw, density=2.0)
        plt.show()

class Example10(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, x, y, delta, mu):
        return 1*y - 2*1*x, 2*1*x - 1*y
    
    def drawPhasePortrait(self, title):
        super().drawPhasePortrait(self, title)

    def drawPhasePortraitNoParameters(self, title):
        self.configurePlot()
        dX, dY = self.calculatePhasePortrait(self.X, self.Y, 0, 0)
        speed = np.sqrt(dX**2 + dY**2)
        lw = 5*speed / speed.max()
        plt.streamplot(self.X, self.Y, dX, dY, color='r', linewidth=lw, density=2.0)
        plt.show()

class Example11(genericExercise):
    def __init__(self, numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition) -> None:
        super().__init__(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)

    def configurePlot(self):
        super().configurePlot()

    def parameterCases(self):
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)
        parametersCase = {'mu':1.0, 'delta':1.0}
        self.parameters.append(parametersCase)

    def calculatePhasePortrait(self, x, y, delta, mu):
        return 3*x - 6*y, -7*y + (x*y - y**2)
    
    def drawPhasePortrait(self, title):
        super().drawPhasePortrait(self, title)

    def drawPhasePortraitNoParameters(self, title):
        self.configurePlot()
        dX, dY = self.calculatePhasePortrait(self.X, self.Y, 0, 0)
        speed = np.sqrt(dX**2 + dY**2)
#        lw = 5*speed / speed.max()
        lw = 1
        seek_points = np.array([[14],[0.0250]])
        plt.streamplot(self.X, self.Y, dX, dY, color='r', linewidth=lw, density=5.0, start_points = seek_points.T)

        self.axes.plot(seek_points[0], seek_points[1], 'bo')
        self.axes.set(xlim =(0, 55), ylim =(0, 30))
        plt.show()

'''
numPlotsPerColumn = 2
numPlotsPerRow = 3
figHorizontalSize = 18
figVerticalSize = 9
plotSizeLength = 1
textVerticalPosition = 0.83 * plotSizeLength
#exercise1 = Exercise1(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)
#exercise1.drawPhasePortrait('Problem 1.6.1a - Non Degenerate Cases')

numPlotsPerColumn = 2
numPlotsPerRow = 4
figHorizontalSize = 18
figVerticalSize = 9
plotSizeLength = 2
textVerticalPosition = 0.83 * plotSizeLength
#exercise2 = Exercise2(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)
#exercise2.drawPhasePortrait('Problem 1.6.1a - Degenerate Cases')

numPlotsPerColumn = 2
numPlotsPerRow = 3
figHorizontalSize = 18
figVerticalSize = 9
plotSizeLength = 2
textVerticalPosition = 0.83 * plotSizeLength
#exercise3 = Exercise3(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)
#exercise3.drawPhasePortrait('Problem 1.6.1e - Non Degenerate Cases')

numPlotsPerColumn = 2
numPlotsPerRow = 3
figHorizontalSize = 18
figVerticalSize = 9
plotSizeLength = 5
textVerticalPosition = 0.83 * plotSizeLength
#exercise4 = Exercise4(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)
#exercise4.drawPhasePortrait('Problem 1.6.1d - Non Degenerate Cases')

numPlotsPerColumn = 2
numPlotsPerRow = 3
figHorizontalSize = 18
figVerticalSize = 9
plotSizeLength = 1.2
textVerticalPosition = 0.83 * plotSizeLength
exercise4 = Exercise5(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)
exercise4.drawPhasePortrait('Problem 1.6.1f')

numPlotsPerColumn = 1
numPlotsPerRow = 1
figHorizontalSize = 18
figVerticalSize = 9
plotSizeLength = 1.5
textVerticalPosition = 0.83 * plotSizeLength
example7 = Example7(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)
example7.drawPhasePortraitNoParameters('Problem 1.6.1f')

numPlotsPerColumn = 1
numPlotsPerRow = 1
figHorizontalSize = 18
figVerticalSize = 9
plotSizeLength = 1.5
textVerticalPosition = 0.83 * plotSizeLength
example8 = Example8(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)
example8.drawPhasePortraitNoParameters('Problem 1.6.1f')
'''

numPlotsPerColumn = 1
numPlotsPerRow = 1
figHorizontalSize = 18
figVerticalSize = 9
plotSizeLength = 50
textVerticalPosition = 0.83 * plotSizeLength
example = Example11(numPlotsPerColumn, numPlotsPerRow, figHorizontalSize, figVerticalSize, plotSizeLength, textVerticalPosition)
example.drawPhasePortraitNoParameters('Problem 1.6.1f')
