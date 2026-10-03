import inspect
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

import pyfirmata

arduino = pyfirmata.Arduino('COM7')
def acenderLED():
    led = arduino.digital[13]
    led.write(1)  #Acender LED

def apagarLED():
    led = arduino.digital[13]
    led.write(0)   #Apagar LED




