import os
from PyLTSpice.LTSpiceBatch import SimCommander

meAbsPath = os.path.dirname(os.path.abspath(__file__))

LTC = SimCommander(meAbsPath + "/" + "testCircuit.asc")
LTC.run()
LTC.wait_completion()

