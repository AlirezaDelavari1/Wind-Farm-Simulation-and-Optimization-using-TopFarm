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
n_wd = 16

iea37 = IEA37_WindTurbines() #3.35MW 
v80 = V80() #V80
dtu10mw = DTU10MW() #DTU10MW

site = IEA37Site(n_wt)
wt = IEA37_WindTurbines()
wd = np.linspace(0. , 360. , n_wd, endpoint=False)
wfmodel = IEA37SimpleBastankhahGaussian(site, wt)

# #wind turbines specs
# wts = WindTurbines.from_WindTurbine_lst([v80,iea37,dtu10mw])
# types = wts.types()
# print ("Name:\t\t%s" % "\t".join(wts.name(types)))
# print('Diameter[m]\t%s' % "\t".join(map(str,wts.diameter(type=types))))
# print('Hubheigt[m]\t%s' % "\t".join(map(str,wts.hub_height(type=types))))

# #plot power curves
# ws = np.arange(3,25)
# plt.xlabel('Wind speed [m/s]')
# plt.ylabel('Power [kW]')

# for t in types:
#     plt.plot(ws, wts.power(ws, type=t)*1e-3,'.-', label=wts.name(t))
# plt.legend(loc=1)
# plt.show()
# #Plot CT curves
# plt.xlabel('Wind speed [m/s]')
# plt.ylabel('CT [-]')

# for t in types:
#     plt.plot(ws, wts.ct(ws, type=t),'.-', label=wts.name(t))
# plt.legend(loc=1)
# plt.show()

# #########################

# #Plot wind rose
# plt.figure(figsize=(8, 8))
# site.plot_wd_distribution(n_wd=12)
# plt.title(f'Hornsrev1 Site Wind Rose')
# plt.show()

# #Plotting wind rose
# plotWR = site.plot_wd_distribution(n_wd=12, ws_bins=[0,5,10,15,20,25])
# plt.title(f'IEA37 Site Wind Rose')
# plt.show()

# #Plotting probability density function
# plotWS = site.plot_ws_distribution(wd=[0,90,180,270])
# plt.title(f'IEA37 Site probability density function')
# plt.show()

# #########################

cost_comp = PyWakeAEPCostModelComponent(wfmodel, n_wt, wd=wd)

initial = get_iea37_initial(n_wt)
driver = EasyScipyOptimizeDriver()
design_vars = dict(zip('xy', (initial[:, :2]).T))

tf_problem = TopFarmProblem(
            design_vars,
            cost_comp,
            constraints = get_iea37_constraints(n_wt),
            driver=driver,
            plot_comp=XYPlotComp()
)

_, state, _ = tf_problem.optimize()


from py_wake.examples.data.iea37 import IEA37Site, IEA37_WindTurbines
from py_wake.literature.gaussian_models import Bastankhah_PorteAgel_2014


optimized_x, optimized_y = state['x'], state['y']

wdir = 270
wsp = 9.8

wf_model = Bastankhah_PorteAgel_2014(site, wt, k=0.0324555)
sim_res = wf_model(
    x=optimized_x, 
    y=optimized_y, 
)


flow_map = sim_res.flow_map(grid=None, 
                          wd=wdir,
                          ws=wsp)


plt.figure()
flow_map.plot_wake_map()
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('Wake map for optimized layout - ' + f' {wdir} deg and {wsp} m/s')
plt.show(block=True)

