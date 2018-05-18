from riconoscimento_gesti.detezione_movimento import MotionDetector
from riconoscimento_gesti.detezione_gesti import GestureDetector
import numpy as np
import cv2
import imutils
import argparse

#argomenti da riga di comando
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dev", required=True, help="indice della sorgente video")
ap.add_argument("-b", "--box", required=True, help="top, right, botton, left cordinate")
ap.add_argument("-v", "--video", required=False, help="se vuoi il video metti il path")
args = vars(ap.parse_args())

def nothing(x):
    pass

#finestra nella quale verranno agganciati gli slider
cv2.namedWindow("ok")

#definisco i range del colore hsv che voglio modifcare
#manualemtne tramite gli slider
cv2.createTrackbar("Tonalità bassa", "ok", 2, 178, nothing)
cv2.createTrackbar("Tonalità alta", "ok", 13, 178, nothing)
cv2.createTrackbar("Saturazione bassa", "ok", 48, 255, nothing)
cv2.createTrackbar("Saturazione alta", "ok", 195, 255, nothing)
cv2.createTrackbar("Luminosità_bassa", "ok", 0, 255, nothing)
cv2.createTrackbar("Luminosità alta", "ok", 255, 255, nothing)

#faccio il check del video se non c'è uso la camera
if not args.get("video", False):
    camera = cv2.VideoCapture(int(args["dev"]))
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

    #range per hue ovvero il colore
    low_h  = cv2.getTrackbarPos('Tonalità bassa', 'ok');
    high_h = cv2.getTrackbarPos('Tonalità alta', 'ok');
    #range per la saturazione
    low_s = cv2.getTrackbarPos('Saturazione bassa', 'ok');
    high_s = cv2.getTrackbarPos('Saturazione alta', 'ok');
    #range per il value ovvero luminosita
    low_v = cv2.getTrackbarPos('Luminosità_bassa', 'ok');
    high_v = cv2.getTrackbarPos('Luminosità alta', 'ok');

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
    #estraggo l'elemeneto desiderato tramite il colore
    gray = md.skindetect(roi, low_h, low_s, low_v, high_h, high_s, high_v)

    #accumolo i pesi per la futura analisi
    if numFrames < 32:
        md.update(gray)
    else:
        #gray = md.skindetect(roi)
        hand = md.detect(gray)
        
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

