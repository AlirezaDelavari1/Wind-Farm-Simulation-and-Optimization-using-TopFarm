import numpy as np
import matplotlib.pyplot as plt 

from py_wake.deficit_models.gaussian import IEA37SimpleBastankhahGaussian 
from py_wake.examples.data.iea37 import IEA37_WindTurbines , IEA37Site
from topfarm.cost_models.py_wake_wrapper import PyWakeAEPCostModelComponent
from topfarm import TopFarmProblem
from topfarm.easy_drivers import EasyScipyOptimizeDriver
from topfarm.examples.iea37 import get_iea37_initial , get_iea37_constraints , get_iea37_cost
from topfarm.plotting import NoPlot , XYPlotComp
from py_wake.examples.data.hornsrev1 import V80
from py_wake.examples.data.dtu10mw import DTU10MW
from py_wake.examples.data.hornsrev1 import Hornsrev1Site
from py_wake.wind_turbines import WindTurbine, WindTurbines

n_wt = 9
site1 = IEA37Site(n_wt)
site2 = Hornsrev1Site(n_wt)


#Plot wind rose of IEA37
plt.figure(figsize=(8, 8))
site1.plot_wd_distribution(n_wd=12)
plt.title(f'IEA37 Site Wind Rose')
plt.show()
#Plot wind rose of Hornsrev1
plt.figure(figsize=(8, 8))
site2.plot_wd_distribution(n_wd=12)
plt.title(f'Hornsrev1 Site Wind Rose')
plt.show()

#Plotting wind rose of IEA37
plotWR = site1.plot_wd_distribution(n_wd=12, ws_bins=[0,5,10,15,20,25])
plt.title(f'IEA37 Site Wind Rose')
plt.show()
#Plotting wind rose of Hornsrev1
plotWR = site2.plot_wd_distribution(n_wd=12, ws_bins=[0,5,10,15,20,25])
plt.title(f'Hornsrev1 Site Wind Rose')
plt.show()

#Plotting probability density function of IEA37
plotWS = site1.plot_ws_distribution(wd=[0,90,180,270])
plt.title(f'IEA37 Site probability density function')
plt.show()
#Plotting probability density function of Hornsrev1
plotWS = site2.plot_ws_distribution(wd=[0,90,180,270])
plt.title(f'Hornsrev1 Site probability density function')
plt.show()
