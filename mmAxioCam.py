import sys
import os

COMPORT = 'COM1'
ANSWERTIMEOUT = '100'
BAUDRATE = '57600'
AXIO = 'Axio'
FOCUS = 'ZeissFocusAxis'

# Load Micro Manager Core
MMPATH = os.path.abspath("C:\Program Files\Micro-Manager-1.4")
sys.path.append(MMPATH)
import MMCorePy
mmc = MMCorePy.CMMCore()

# Add COM port.
mmc.loadDevice(COMPORT, 'SerialManager', COMPORT)
mmc.setSerialProperties('COM1', ANSWERTIMEOUT, BAUDRATE, '0', 'Off', 'None', '1')

# Add the microscope base.
mmc.loadDevice(AXIO, 'ZeissCAN29', 'ZeissScope')
mmc.setProperty(AXIO, 'Port', COMPORT)

# Add the Z drive.
mmc.loadDevice(FOCUS, 'ZeissCAN29', 'ZeissFocusAxis')
