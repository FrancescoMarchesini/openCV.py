from pyimagesearch.gesture_recognition.motiondetector import MotionDetector
from pyimagesearch.gesture_recognition.gesturedetector import GestureDetector
import numpy as np
import cv2
import imutils
import argparse

#argomenti da riga di comando
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--box", required=True,
        help="top, right, botton, left cordinate")
ap.add_argument("-v", "--video", required=False,
        help="se vuoi il video metti il path")
args = vars(ap.parse_args())

#faccio il check del video se non c'è uso la camera
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

#camera.set(3, 1024)
#camera.set(4, 768)

#prendo i valori per la costruzione della ROI
(top, right, bot, left) = np.int32(args["box"].split(","))
print("roi(%d, %d, %d, %d) " %(top, right, bot, left))

#inizializzo la l'instanza della classe motion
md = MotionDetector()
gd = GestureDetector()
#metto il counter dei frame a zero
numFrames = 0
gesture = None
bprint = True
values = []

#main loop
while True:
    #prendo i frame e li salvo nella variabile frame e variabilie di controllo grabbed
    (grabbed, frame) = camera.read()

    #check se ce lo stream
    if args.get("video") and not grabbed:
            break;

    #faccio il resize dello stream
    frame = imutils.resize(frame, width=600)
    #inverto l'immagine in modo da avera la mano sinistra alla portata
    frame = cv2.flip(frame, 1)
    #copio l immagine originale sulla quale andro poi a disegnare
    clone = frame.copy()
    #salvo in due varibile la dimensioni dell'immagine
    (frameW, frameH) = frame.shape[:2]

    #estraggo la ROI dall'immagine
    roi = frame[top:bot, right:left]
    #converto la ROI in scala di grigi
    #gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    #applico un filtro blurred con lernel 7x7 per migliorare i contorni
    gray = md.skindetect(roi)
    #gray = cv2.GaussianBlur(gray, (7, 7), 0) 
    #cv2.imshow("skin", gray)

    #accumolo i pesi per la futura analisi
    if numFrames < 32:
        md.update(gray)

    #applico il threshold per rilevare i contorni allinterno della roi
    else:
        #gray = md.skindetect(roi)
        hand = md.detect(gray, 25, 15)
        
        #faccio il check se e stato preseo il movimento
        if hand is not None:
            #salvo in un tupla i valori di ritorno del detect ovvero l'immagine di threshold
            #e i relativi contorni
            (thresh, c) = hand
            #disegno i contorni sull immagine tralandoli quindi della dimensione della ROI
            cv2.drawContours(clone, [c+(right, top)], -1, (0, 255, 0), 2)
            #le dita
            fingers = gd.detect(clone, thresh, c)

            #check sulle dita ed inizializzo
            if gesture is None:
                gesture = [1, fingers]

            #inizio a contare le dita
            else:
                if gesture[1] == fingers:
                    gesture[0] += 1

                    #se raggiungo un sufficente numero di frame, scrvio il numero
                    if gesture[0] >= 25:
                        #se il valore e pieno lo metto a zero
                        if len(values) == 2:
                            values = []

                            #faccio lupdate del valore delle dita
                            values.append(fingers)
                            gesture = None
                            print(values)
                else:
                    gesture = None
            
            #disegno per chiarificazione il threshold
            cv2.imshow("thresh", thresh)
  
    if len(values) > 0 :
        GestureDetector.drawBox(clone, 0)
        GestureDetector.drawText(clone, 0, values[0])
        GestureDetector.drawText(clone, 1, "+")
        
    if len(values) == 2:
        GestureDetector.drawBox(clone, 2)
        GestureDetector.drawText(clone, 2, values[1])
        GestureDetector.drawText(clone, 3, "=")
        GestureDetector.drawBox(clone, 4, color=(0, 255, 0))
        GestureDetector.drawText(clone, 4, values[0] + values[1], color=(0, 255, 0))

    
    #disgeno la roi
    cv2.rectangle(clone, (left, top), (right, bot), (0, 0, 255), 2)
    #aumento il numero di frame
    numFrames += 1

    #visualizzo l immagine
    cv2.imshow("ok", clone)
    #condizione di uscita da input di tastiera tasto q
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

