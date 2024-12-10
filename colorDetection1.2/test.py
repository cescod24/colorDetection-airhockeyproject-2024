import serial
import time


ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(0.5) 

diameter = 4
pi = 3.1416
circum = diameter * pi

start_x1 = 0
start_y1 = 0
steps_10 = 0
steps_20 = 0

width = 1328
height = 800
error_x = 93 #0,0 non è a 1328 ma a 1328 - 93
max_x = 580
error_y = 100
max_y = 700

# circum * dpassi / 400 = Dx --> Dx * 400 / circum = dpassi da fare
# 0,0 angolo basso a sinistra
# motore sinistro orario -dx -dy
# motore destro orario dx -dy width 100 cm height 60cm 
# per trasformarlo sulle coordinate motore fai (width - x, height - y)

'''def calculateSteps(x, y, x0, y0):

    x = (x / 1328) * 100
    x0 = (x0 / 1328) * 100
    y = (y / 800) * 60
    y0 = (y0 / 800) * 60

    dx = x - x0
    dy = y - y0

    steps1x = (- dx * 400 / circum)
    steps1y = (- dy * 400 / circum) 
    steps2x = (dx * 400 / circum) 
    steps2y = (- dy * 400 / circum) 

    steps1 = int((steps1x + steps1y) / 2)
    steps2 = int((steps2x + steps2y) / 2)

    print(steps1, steps2, steps_10, steps_20, steps1x, steps1y)

    return steps1, steps2'''

    
while True:
    
    x = input("Inserisci x: ")
    y = input("Inserisci y: ")
    x = int(x)
    y = int(y)

    if 0 <= x <= max_x and 0 <= y <= max_y:

        '''steps1, steps2 = calculateSteps(x, y, start_x1, start_y1)
        start_x, start_y = x, y
        steps_10, steps_20 = steps1, steps2'''

        ser.write(f'{x} {y} move\n'.encode())

        """risposta = ser.readline().decode('ascii').strip()
        if risposta:
            print(f"Arduino ha risposto: {risposta}")

        interpolazione = ser.readline().decode('ascii').strip()
        if interpolazione:
            print(f"interpolazione: {interpolazione}")

        movimento = ser.readline().decode('ascii').strip()
        if movimento:
            print(f"interpolazione: {movimento}")"""

    else:
        print("Per favore, inserisci solo numeri.")
