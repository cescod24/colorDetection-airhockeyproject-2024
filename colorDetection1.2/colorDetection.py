
import cv2 
import numpy as np
from PIL import Image
import math
import serial
import time


cap = cv2.VideoCapture(1)
imgPicker = np.zeros((200,400,3), np.uint8)

width = 3448  # Larghezza desiderata
height = 808 # Altezza desiderata
cutGreen = 48
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

fps = 60  # FPS desiderati
cap.set(cv2.CAP_PROP_FPS, fps)

actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
actual_fps = cap.get(cv2.CAP_PROP_FPS)

height_cut = 800
width_cut = 1328

poleUp = 150
poleDown = 700


print(f"Risoluzione impostata: {width}x{height}")
print(f"FPS impostati: {fps}")
print(f"Risoluzione effettiva: {actual_width}x{actual_height}")
print(f"FPS effettivi: {actual_fps}")

global callbackable
callbackable = True

listCleared = False

colorBGRMin = np.array([[[0,0,0]]], np.uint8) #creo un colore come se fosse un' immagine da un pixel con 3 canali
colorBGRMax = np.array([[[0,0,0]]], np.uint8) #uguale a sopra ma per hsv
colorHSVMin = np.array([[[0,0,0]]], np.uint8)
colorHSVMax = np.array([[[0,0,0]]], np.uint8)  

points = []
speeds = []
accelerations = []
goals = []
crosses = []
scarto = 5
raggioDisco = 40 #per l'errore della fotocamera
erroreBordo = 15
cross_x = 800

#MOTORI

motorSpeed = 1500
motorMaxSpeed = 7000
motorAccel = 30000
circum = 3.1416 * 0.04 #m
start_x = 20
start_y = 330
pos_x = start_x
pos_y = start_y
tMinor = True
raggioPusher = 35

error_x = 1250 # intervallo x[1250, 750] --> [0, 500] quindi x' = -x + 1250
max_x = 500 #Verificato!!!
error_y = 80 # intervallo y[80, 720] --> y'[650, 0] quindi y' = -65/64 y + 731.25
max_y = 650 #verificato!!
threshold = 10


ser = serial.Serial('COM3', baudrate=9600, timeout=1)
time.sleep(2)
preparing = True
ser.write(f'{start_x} {start_y}\n'.encode())
while preparing:
    response = ser.readline().decode('ascii').strip()
    if response == "ready":
        print(response)
        preparing = False
        break


def changeHSVMin(x):

    global callbackable
    if not callbackable:
        return 1
    
    h = cv2.getTrackbarPos('H_MIN', 'color picker')
    s = cv2.getTrackbarPos('S_MIN', 'color picker')
    v = cv2.getTrackbarPos('V_MIN', 'color picker')

    colorHSVMin[:] = [[h, s, v]]

    BGRColor = cv2.cvtColor(colorHSVMin, cv2.COLOR_HSV2BGR)

    callbackable = False
    cv2.setTrackbarPos('R_MIN', 'color picker', BGRColor[0][0][2])
    cv2.setTrackbarPos('G_MIN', 'color picker', BGRColor[0][0][1])
    cv2.setTrackbarPos('B_MIN', 'color picker', BGRColor[0][0][0])

    r = cv2.getTrackbarPos('R_MIN', 'color picker')
    g = cv2.getTrackbarPos('G_MIN', 'color picker')
    b = cv2.getTrackbarPos('B_MIN', 'color picker')

    cv2.rectangle(imgPicker, (0,0), (200,200), (b, g, r), -1)
    cv2.putText(imgPicker, 'min', (0,25), 0, 1, (0, 0, 0), 2, )
    callbackable = True

    return 0

def changeBGRMin(y):

    global callbackable
    if not callbackable:
        return 1
    
    r = cv2.getTrackbarPos('R_MIN', 'color picker')
    g = cv2.getTrackbarPos('G_MIN', 'color picker')
    b = cv2.getTrackbarPos('B_MIN', 'color picker')

    colorBGRMin[:] = [[b, g, r]]
    HSVColor = cv2.cvtColor(colorBGRMin, cv2.COLOR_BGR2HSV) #converto il colore come se fosse un pixel di un' immagine con 3 canali
    callbackable = False
    cv2.setTrackbarPos('H_MIN', 'color picker', HSVColor[0][0][0])
    cv2.setTrackbarPos('S_MIN', 'color picker', HSVColor[0][0][1])
    cv2.setTrackbarPos('V_MIN', 'color picker', HSVColor[0][0][2])
    cv2.rectangle(imgPicker, (0,0), (200,200), (b,g,r),-1)
    cv2.putText(imgPicker, 'min', (0,25), 0, 1, (0, 0, 0), 2, )
    callbackable = True

    return 0

def changeBGRMax(z):

    global callbackable
    if not callbackable:
        return 1
    
    r = cv2.getTrackbarPos('R_MAX', 'color picker')
    g = cv2.getTrackbarPos('G_MAX', 'color picker')
    b = cv2.getTrackbarPos('B_MAX', 'color picker')

    colorBGRMax[:] = [[b, g, r]]
    HSVColor = cv2.cvtColor(colorBGRMax, cv2.COLOR_BGR2HSV) #converto il colore come se fosse un pixel di un' immagine con 3 canali
    callbackable = False
    cv2.setTrackbarPos('H_MAX', 'color picker', HSVColor[0][0][0])
    cv2.setTrackbarPos('S_MAX', 'color picker', HSVColor[0][0][1])
    cv2.setTrackbarPos('V_MAX', 'color picker', HSVColor[0][0][2])
    cv2.rectangle(imgPicker, (200,0), (400,200), (b,g,r),-1)
    cv2.putText(imgPicker, 'max', (330,25), 0, 1, (0, 0, 0), 2, )
    callbackable = True

    return 0

def changeHSVMax(q):

    global callbackable
    if not callbackable:
        return 1
    
    h = cv2.getTrackbarPos('H_MAX', 'color picker')
    s = cv2.getTrackbarPos('S_MAX', 'color picker')
    v = cv2.getTrackbarPos('V_MAX', 'color picker')

    colorHSVMax[:] = [[h, s, v]]

    BGRColor = cv2.cvtColor(colorHSVMax, cv2.COLOR_HSV2BGR)

    callbackable = False
    cv2.setTrackbarPos('R_MAX', 'color picker', BGRColor[0][0][2])
    cv2.setTrackbarPos('G_MAX', 'color picker', BGRColor[0][0][1])
    cv2.setTrackbarPos('B_MAX', 'color picker', BGRColor[0][0][0])

    r = cv2.getTrackbarPos('R_MAX', 'color picker')
    g = cv2.getTrackbarPos('G_MAX', 'color picker')
    b = cv2.getTrackbarPos('B_MAX', 'color picker')

    cv2.rectangle(imgPicker, (200,0), (400,200), (b, g, r), -1)
    cv2.putText(imgPicker, 'max', (330,25), 0, 1, (0, 0, 0), 2, )
    callbackable = True

    return 0

def colorPickerTrackbar():

    cv2.namedWindow('color picker') 
    cv2.createTrackbar('R_MIN', 'color picker', 0, 255, changeBGRMin)
    cv2.createTrackbar('G_MIN', 'color picker', 0, 255, changeBGRMin)
    cv2.createTrackbar('B_MIN', 'color picker', 0, 255, changeBGRMin)
    cv2.createTrackbar('R_MAX', 'color picker', 0, 255, changeBGRMax)
    cv2.createTrackbar('G_MAX', 'color picker', 0, 255, changeBGRMax)
    cv2.createTrackbar('B_MAX', 'color picker', 0, 255, changeBGRMax)
    cv2.createTrackbar('H_MIN', 'color picker', 0, 179, changeHSVMin)
    cv2.createTrackbar('S_MIN', 'color picker', 0, 255, changeHSVMin)
    cv2.createTrackbar('V_MIN', 'color picker', 0, 255, changeHSVMin)
    cv2.createTrackbar('H_MAX', 'color picker', 0, 179, changeHSVMax)
    cv2.createTrackbar('S_MAX', 'color picker', 0, 255, changeHSVMax)
    cv2.createTrackbar('V_MAX', 'color picker', 0, 255, changeHSVMax)
    cv2.resizeWindow('color picker', 400, 400)

    cv2.setTrackbarPos('R_MIN', 'color picker', 120)
    cv2.setTrackbarPos('G_MIN', 'color picker', 25)
    cv2.setTrackbarPos('B_MIN', 'color picker', 25)
    cv2.setTrackbarPos('R_MAX', 'color picker', 255)
    return 0

def calculateAccelAndSpeed(lastSpeed):
    
    if len(points) > 4:

        speed = round(math.sqrt(((points[0][0] - points[-1][0]) / 800 * 0.6) ** 2 + ((points[0][1] - points[-1][1]) / 800 * 0.6)** 2) / (points[-1][2] - points[0][2]), 5)
        if speed < lastSpeed:
            lastSpeed = speed
        #avgAccel = round(sum(accelerations) / len(accelerations), 4) if len(accelerations) != 0 else 0
    return lastSpeed

def predictTrajectory(center_x, center_y, frame): #trendline source: https://classroom.synonym.com/calculate-trendline-2709.html
    
    rimbalzi = 0

    avgGoal = 0
    avgCross = 0
    distanceToCross = 0
    rebounded = False

    if len(points) > 4:

        a = 0
        sum_x = 0
        sum_y = 0
        sumSquare_x = 0

        n = len(points)

        for point in points:

            a += point[0] * point[1]
            sum_x += point[0]
            sum_y += point[1]
            sumSquare_x += point[0] ** 2
        
        a *= n
        b = sum_x * sum_y
        c = n * sumSquare_x
        d = sum_x ** 2
        
        m = (a - b) / (c - d) if (c - d) != 0 else 0 #pendenza --> ricordarsi che il sistema non rileva punti in verticale
        x = width_cut - cutGreen
        q = (center_y - m * center_x)
        y = int(m * x + q) #considerare che si lavora in (x→+, y↓+)
        
        def calculateStandardError(m, q):
            SumSquaredErrors = 0

            for point in points:
                
                SumSquaredErrors += ((m * point[0] + q) - point[1])**2
            
            StandardError = math.sqrt((SumSquaredErrors) / len(points)) * 100

            return StandardError

        StandardError = calculateStandardError(m, q) 

        if StandardError > 1000:
            del points[:-1]
        
        rebounding = False

        cross_y = 0

        if 0 <= y <= height:
            
            cv2.line(frame, (center_x, center_y), (x, y), (0, 255, 0), 5)

            if 0 <= y < height_cut:
                cross_y = int(m * cross_x + q)
                cv2.circle(frame, (cross_x, cross_y), 10, (255,255,50), 3, 1)
                crosses.append(cross_y)
                goals.append(y)
        else:
            rebounding = True

        firstHit = True
        firstCross = True
        firstHitFirstCross = False
        rebounded = False

        firstBounce_x = 0
        firstBounce_y = 0
        bounce_x = 0
        bounce_y = 0
        bounce_x1 = 0
        bounce_y1 = 0
        goal_x = 0
        goal_y = 0
       
        stop_x = 0
        stop_y = 0

        while rebounding:
            
            if firstCross:
                rimbalzi += 1
            
            if firstHit == True:

                if m < 0:
                    firstBounce_x = int(-q / m) - raggioDisco
                    firstBounce_y = 0 + raggioDisco
                else: # m>0
                    firstBounce_x = int((height - q) / m) - raggioDisco
                    firstBounce_y = height - raggioDisco
                
                cv2.line(frame, (center_x, center_y), (firstBounce_x, firstBounce_y), (0, 255, 0), 5)

                if firstBounce_x >= cross_x and firstCross: #calcola dove ha l'intersezione con un punto x deciso da noi
                
                    stop_x, stop_y = firstBounce_x, firstBounce_y
                    cross_y = int((m * cross_x + q))
                    crosses.append(cross_y)
                    cv2.circle(frame, (cross_x, cross_y), 10, (255,255,50), 3, 1)
                    firstCross = False
                    firstHitFirstCross = True

                bounce_x, bounce_y = firstBounce_x, firstBounce_y
                firstHit = False

            m *= -1
            q = (bounce_y - m * bounce_x)

            if m < 0:
                bounce_x1 = int(-q / m) - raggioDisco
                bounce_y1 = 0 + raggioDisco
            else: # m>0
                bounce_x1 = int((height - q) / m) - raggioDisco
                bounce_y1 = height - raggioDisco

            if bounce_x < 0 or bounce_y < 0 or bounce_x1 < 0 or bounce_y1 < 0:
                print("Errore: coordinate negative")
                break

            if bounce_x1 >= cross_x and firstCross: #calcola dove ha l'intersezione con un punto x deciso da noi
                
                stop_x, stop_y = bounce_x, bounce_y
                cross_y = int((m * cross_x + q))
                crosses.append(cross_y)

                cv2.circle(frame, (cross_x, cross_y), 10, (255,255,50), 3, 1)

                firstCross = False

            if firstBounce_x < cross_x or bounce_x < cross_x or bounce_x1 < cross_x:
                rebounded = True
                            
            if bounce_x1 >= width_cut - cutGreen - raggioDisco: #bounce_xy1 diventano il goal

                goal_x = width_cut - cutGreen
                goal_y = int((m * goal_x + q)) + raggioDisco if m > 0 else int((m * goal_x + q)) - raggioDisco

                if poleUp < goal_y < poleDown:

                    goals.append(goal_y)
                            
                try:
                    cv2.line(frame, (bounce_x, bounce_y), (bounce_x1, bounce_y1), (255, 120, 120), 5)
                except UnboundLocalError:
                    print("Unbound Local Error: passed to the next iteration")
                       
                break
            
            try:
                cv2.line(frame, (bounce_x, bounce_y), (bounce_x1, bounce_y1), (255, 0, 0), 5)
            except UnboundLocalError:
                print("Unbound Local Error: passed to the next iteration")

            bounce_x, bounce_y = bounce_x1, bounce_y1

        def calculateGoalAvg(goals):

            geometricGoalAvg = 1

            if len(goals) > 0:

                for goal in goals: geometricGoalAvg *= goal if goal > 0 else 1

                geometricGoalAvg = int(geometricGoalAvg ** (1 / len(goals))) 

            return geometricGoalAvg
            
        def calculateCrossAvg(crosses):

            avgCross = 1

            if len(crosses) > 0:

                for cross in crosses: avgCross *= cross if cross > 0 else 1

                avgCross = int(avgCross ** (1 / len(crosses))) 

            return avgCross
        
        avgGoal = calculateGoalAvg(goals)
        avgCross = calculateCrossAvg(crosses)
        
        if rebounding and not firstHitFirstCross:
            distanceToCross = math.sqrt(((center_x - firstBounce_x) / 800 * 0.6) ** 2 + ((center_y - firstBounce_y) / 800 * 0.6) ** 2) + (rimbalzi - 1) * math.sqrt(((bounce_x - bounce_x1) / 800 * 0.6) ** 2 + ((bounce_y - bounce_y1) / 800 * 0.6) ** 2) + math.sqrt(((stop_x - cross_x) / 800 * 0.6) ** 2 + ((stop_y - avgCross) / 800 * 0.6) ** 2)
        else:
            distanceToCross = math.sqrt(((center_x - cross_x) / 800 * 0.6) ** 2 + ((center_y - avgCross) / 800 * 0.6) ** 2)
        
        distanceToCross = round(distanceToCross, 2)
    
    return avgGoal, avgCross, distanceToCross, rebounded
    
def draw_points(frame, center_x, center_y, goal):

    for point in points:
        cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)

    cv2.putText(frame, f'{center_x, center_y}', (50, 100), 1, 4, (255, 125, 125), 3)
    cv2.putText(frame, f'{goal}', (650, 100), 1, 4, (255, 0, 125), 3)

def calculateTCross(v0, distanceToCross, rebounded): #è mrua ma lo tratto come mru visto che calcolo ogni frame un punto
    
    t = distanceToCross / v0
    if rebounded:
        t *= 1.25
    return t

def sendArduino(t, cross_x, cross_y, tMinor, pos_x, pos_y):

    if len(points) < 5:

        return tMinor, pos_x, pos_y

    if cross_x != 0 and cross_y != 0 and t != 0:
        
        r_tot = raggioPusher + raggioDisco - erroreBordo #calcola il displacement per mandare sempre in porta
        halfGoal = height_cut / 2
        angle = math.atan(abs(cross_y - halfGoal) / cross_x)
        displacement = r_tot * math.sin(angle)

        hit_x = int(-cross_x + 1250)
        hit_y = int((-65 / 64) * (cross_y + displacement) + 731.25)
         
        print(f'angle = {angle}, displacement = {displacement}, hit_y = {hit_y}')

        if 0 <= hit_x <= max_x and 0 <= hit_y <= max_y:

            pusherSpeed_x = (motorMaxSpeed / 200) * circum #calcola il tempo per raggiungere cross_x. Considero che si muova mru vista la grandissima accelerazione
            pusherSpeed_y = (motorSpeed / 200) * circum #calcola il tempo per raggiungere cross_x. Considero che si muova mru vista la grandissima accelerazione
            
            tReachCross_y = (hit_y - pos_y) / 650 * 0.4875 / pusherSpeed_y
            tReachCross_x = (hit_x - pos_x) / 500 * 0.375 / pusherSpeed_x
            totalTime = tReachCross_x + tReachCross_y

            if abs(hit_y - pos_y) > threshold and not tMinor:
                ser.write(f'{pos_x} {hit_y} move\n'.encode()) #muove i motori alla giusta posizione per lo strike
                pos_y = hit_y
            
            startTime = points[0][2]
            elapsedTime = time.perf_counter() - startTime
            #print(f'time to reach cross = {totalTime}')
            if (t <= totalTime or elapsedTime <= totalTime) and not tMinor:
                hit_x = 150 if hit_x + 150 < max_x else hit_x
                ser.write(f'{hit_x} {pos_y} strike\n'.encode())
                print(tMinor, pos_x, pos_y) 
                pos_x = start_x
                pos_y = start_y
                tMinor = True

            '''response = ser.readline().decode('ascii').strip()
            if response:
                print(response)'''

    return tMinor, pos_x, pos_y

def main():

    colorPickerTrackbar()
    first = True
    listCleared = False
    lastSpeed = float('inf')

    #MOTORI

    pos_x = start_x
    pos_y = start_y
    hit_x = 0
    hit_y = 0
    tMinor = True
    timer = 0
    otherSide = False
    thrownAway = False
    rebounded = False

    while True:

        ret, frame = cap.read()

        if not ret:
            print("errore lettura frame (firmware installato?)")
            break
        
        #cv2.namedWindow("resized", cv2.WINDOW_NORMAL)
        #cv2.resizeWindow("resized", int(width * 1), int(height * 1))
        
        #taglia il frame
        frame = frame[0:height_cut, cutGreen:width_cut] #adattamento alla camera sony
        
        #maschera
        lowerLimit = np.array([cv2.getTrackbarPos('H_MIN', 'color picker'), 
                    cv2.getTrackbarPos('S_MIN', 'color picker'), 
                    cv2.getTrackbarPos('V_MIN', 'color picker')])
        upperLimit = np.array([cv2.getTrackbarPos('H_MAX', 'color picker'), 
                    cv2.getTrackbarPos('S_MAX', 'color picker'), 
                    cv2.getTrackbarPos('V_MAX', 'color picker')])
        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        result = cv2.bitwise_and(frame, frame, mask=mask) #mostra solo i frame della maschera

        mask_ = Image.fromarray(mask)
        bbox = mask_.getbbox()

        if bbox is not None:
            x1, y1, x2, y2 = bbox

            center_x, center_y = (x2 + x1) // 2, (y2 + y1) // 2

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.circle(frame, (center_x, center_y), 10, (255, 0, 0), -1)

            if first: #prima iterazione in assoluto
                oldCenter_x = 0
                lastSpeed = float('inf')
                first = False

            if (center_x <= oldCenter_x + scarto and not listCleared): #il disco è stato rimandato di là

                accelerations.clear()
                points.clear()
                goals.clear()
                crosses.clear()

                listCleared = True
                tMinor = False

            elif center_x >= oldCenter_x + scarto: #il disco sta andando verso destra...

                startTime = time.perf_counter()
                points.append([center_x, center_y, startTime])
                currentSpeed = calculateAccelAndSpeed(lastSpeed)
                goal, cross_y, distanceToCross, rebounded = predictTrajectory(center_x, center_y, frame)
                timeToCross = calculateTCross(currentSpeed, distanceToCross, rebounded)
                if timeToCross: print(f't = {timeToCross}s, DX = {distanceToCross * 100}cm, v0 = {currentSpeed}m/s')
                

                tMinor, pos_x, pos_y = sendArduino(timeToCross, cross_x, cross_y, tMinor, pos_x, pos_y)
                listCleared = False

            if listCleared and center_x >= 700 and not otherSide and not tMinor:
                
                hit_x = int(-center_x + 1250)
                hit_y = int((-65 / 64) * (center_y) + 731.25)

                if 0 <= hit_x <= max_x and 0 <= hit_y <= max_y:
                    timer = time.perf_counter()
                    print("disco da avversario")
                otherSide = True
            if otherSide and time.perf_counter() - timer > 2 and center_x >= 700 and not thrownAway:
                
                hit_x = int(-center_x + 1250)
                hit_y = int((-65 / 64) * (center_y) + 731.25)

                if 0 <= hit_x <= max_x and 0 <= hit_y <= max_y:
                    print(f'{hit_x}, {hit_y}')
                    ser.write(f'{hit_x} {hit_y} otherSide\n'.encode())
                    thrownAway = True

            if center_x < 600:
                otherSide = False
                thrownAway = False      

            draw_points(frame, center_x, center_y, goal)
            oldCenter_x = center_x

        else:
            first = False  

        cv2.imshow('result', result)
        cv2.imshow('resized', frame)
        cv2.imshow('color picker', imgPicker)

        
        if cv2.waitKey(17) & 0xFF == ord('q'):
            #cv2.imwrite("./wrongcoordinates6.png", frame)
            break
    
    cap.release()
    cv2.destroyAllWindows()
    ser.write(f'0 0 sleep\n'.encode())

if __name__ == "__main__":
    main()

#######################################################################################################
#                                                                                                     #
#                                                                                                     #
# Robotica 2024-2025                                                                                  #
#                                                                                                     #                                                                                           
# Last edit: 29.12.2024 - 12:32                                                                       #
#                                                                                                     #
# @fd                                                                                                 #
#                                                                                                     #
#                                                                                                     #
#######################################################################################################
 
