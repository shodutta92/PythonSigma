from pythonsigma.simulation import Simulation
from time import time


initialValues = [0.1, 10, 10, 10, 10, 10, 10, 3, 3, 3, 3, 3, 3]
datafile = open('data.dat', 'rb')
data_array = {'DATA.DAT': datafile.read().split()}
datafile.close()
sim = Simulation('Model_Enhanced Final.mod', 14400, initialValues, data_array)
time0 = time()
output = sim.run_simulation(12345)
print time() - time0
# print sim.output.statistics['QUEUE[0]']['maximum']