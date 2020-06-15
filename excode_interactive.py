import numpy as np  
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator
from scipy.optimize import curve_fit

#setting up an interactive main menu so that the program can be run easily from the command-line
def mainmenu():
    while True: #so that the user is always returned to the main menu
        print()
        print('''### Main Menu ###
        1. Fit the data using curve_fit and plot in 2D
        2. Fit the data using curve_fit and plot in 3D
        3. Run the simulation to estimate the parameter "a" over a varying number of trials
        ''')
        selection=input("Make Selection: ")
        if selection=="1":
            fit_2d()
        if selection=="2":
            print("N.B.: I have found that often the 3D plot does not work unless I run using 64-bit")
            fit_3d()
        if selection=="3":
            run_sim()
        else:   #to ensure the program does not break when the user makes a typo
            print("Please choose a valid option")   

#initialise the input variables in the range (0,4) with 1000 values
x1=np.linspace(0,4,1000)
x2=np.linspace(0,4,1000)
xdata=np.array([x1,x2])

#define a polynomial function to fit the data
def function(X,a,b,c):
    x1,x2=X
    return a+b*x1+c*x2**2

#define a function to run the curve fit multiple times and extract the averages
def montecarlo(noise_level,number_trials):
    a=[]
    a_err=[]
    for i in range(number_trials):
    #in each trial the y data is set up with random noise added to each pixel
        ydata=function(xdata,1,3,-4)+np.random.normal(0,noise_level,1000)
        popt,pcov=curve_fit(function,xdata,ydata)
        a_err.append(np.sqrt(np.diag(pcov))[0]) #the error on each measurement is calculated from the covariance matrix 
        a.append(popt[0])
    np.asarray(a)
    np.asarray(a_err)
    return np.mean(a),np.mean(a_err)/np.sqrt(number_trials) #the average value and its standard error are returned

#define a function to run the simulation for a varying number of trials and plot the effect on the fitted parameters
def noisetest(minimum_trials=2,maximum_trials=250,simulation_runs=20):
    a=[]
    a_err=[]
    number_trials=np.linspace(minimum_trials,maximum_trials,simulation_runs,dtype=int)   #the variable determining how many trials are completed in each group of measurements
    for i in number_trials:
        a_estimate,a_err_estimate=montecarlo(30,i)  #for each number of trials the simulation is run and the parameter "a" extracted
        a.append(a_estimate)
        a_err.append(a_err_estimate)
    fig,ax=plt.subplots()   #now we can plot the parameter "a" as a function of the number of trials
    ax.scatter(number_trials,a,s=4,color='r')
    ax.errorbar(number_trials,a,a_err,fmt='',color='r')
    plt.axhline(1,linestyle='--',linewidth=0.5,color='k')
    ax.set_xlabel("Number of trials")
    ax.set_ylabel("Best fit of the parameter "+r"$a$")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))   #enforcing integer x-axis labels
    plt.show()

def fit_2d():
    #plot an example of using the curve fit function to verify mechanism
    ydata=function(xdata,1,3,-4)+np.random.normal(0,10,1000)    #artificially constructing some data with random noise added
    popt,pcov=curve_fit(function,xdata,ydata)
    plt.scatter(xdata[0],ydata,s=4,color='r',label="Data")
    plt.plot(xdata[0],function(xdata,*popt),color='b',label="Fit")
    plt.xlabel("Pixel axis 1 (x1)")
    plt.ylabel("Pixel intensity (y)")
    plt.legend()
    plt.show()
    print(popt) #prints the fitted values a,b,c
    print(np.sqrt(np.diag(pcov)))   #prints the errors in the fitted values

def fit_3d():
    print("done")
    #now plot this example in a 3D setting to show variation with multiple variables 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ydata=function(xdata,1,3,-4)+np.random.normal(0,10,1000)    #artificially constructing some data with random noise added
    popt,pcov=curve_fit(function,xdata,ydata)
    ax.scatter(x1, x2, ydata,s=4,color='r',label="Data")
    ax.plot(x1,x2,function(xdata,*popt),color='b',label="Fit")
    ax.set_xlabel("Pixel axis 1 (x1)")
    ax.set_ylabel("Pixel axis 2 (x2)")
    ax.set_zlabel("Pixel intensity (y)")
    plt.legend()
    plt.show()

def run_sim():
    min_trials=int(input("Define mimimum number of trials: "))  #Allow the user to define the min/max number of trials in the test
    if min_trials<1:
        min_trials=2
    max_trials=int(input("Define maximum number of trials: "))
    if max_trials<min_trials:
        max_trials=min_trials+20
    simulation_runs=int(input("Define how many simulations to run: "))  #Allow the user to select how many simulations to run within the selected range of trials
    if simulation_runs<20:
        simulation_runs=20
    noisetest(min_trials,max_trials,simulation_runs)

mainmenu()