from pyimagesearch.gesture_recognition.motiondetector import MotionDetector
from pyimagesearch.gesture_recognition.gesturedetector import GestrureDetector
import numpy as np
import argparse
import imutils
import cv2



#argomenti da riga di comando
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--box", required=True,
	help="top, right, botton, left le cordinate della roi")
ap.add_argument("-v", "--video", required=False, help="se vuoi un vido metti il path")
args = vars(ap.parse_args())

#if non ce il video grabba la camera
if not args.get("video", False):
	camera = cv2.VideoCapture(1)

#altirmenti prendi il video
else:
	camera = cv2.VideoCapture(args["video"])


#setto la roi in base all'input, e inizializzo il motion detecotr
#gesture detection e il counter delle dita
(top, right, bot, left) = np.int32(args["box"].split(","))
md = MotionDetector()
gd = GestureDetection()
numFrames = 0
gestrue = None

#main loop
while True:
	#prendo il frame corrente
	(grabbed, frame) = camera.read()
	#se sto utilizzando il video faccio il check su EOS
	if args.get("video") and not grabbed:
		break

	#prendo il frame lo flippo e lo croppo
	frame = imutils.resize(frame, width=300)
	frame = cv2.flip(frame, 1)
	clone = frame.copy()
	#shape ritorna il numero di righe colonne e canali
        print(frame.shape)
        (frameW, frameH, channel) = frame.shape()

	#setto la roi, passando in right:left 
	roi = frame[top:bot, right:left]
	#faccio il blur
	gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7, 7), 0)

	#applico il motion detection quando ho raggiunto 32 frames
	if numFrames < 32:
		md.update(gray)
        
        else:
            #motion detection
            skin = md.detect(gray, 25, 15)

            #faccio il check se e' stato preso il contonro
            if skin is not None:
                (thresh, c) = skin
                cv2.drawContours(clone, [c + (right, top)], -1, (0, 255, 0), 2)
                fingers = gd.detect(thresh, c)

                #inizializzo l'oggetto dita
                if gesture is None:
                    gesture = [1, fingers]

                #conto delle dita
                else:
                    if gesture[1] == fingers:
                        gesture[0] += 1

                        #ferma la conta se seiamo arrivate a 25 frame
                        if gesture[0] >= 25:
                            if len(values) == 2:
                                values = []

                            values.append(fingers)
                            gesture = None

                    else:
                        gesture = None
    
    #disegno il risultato verificando se ce ne e uno
    if len(values) > 0:
        GestureDetector.drawBox(clone, 0)
        GestureDetector.drawText(clone, 0, values[0])
        GestureDetector.drawText(clone, 1, "+")

    if len(value ) > 2:
        GestureDetector.drawBox(clone, 2)
        GestureDetector.drawText(clone, 2, values[1])
        GestureDetector.drawText(clone, 3, "+")
        GestureDetector.drawText(clone, 4, color=(0, 255, 0))
        GestureDetector.drawText(clone, 4, values[0] + values[1], color=(0, 255, 0))

    #roi per la visualizzazione
    cv2.rectangle(clone, (left, top), (right, bot), (0, 0, 255), 2)
    numFrames += 1

    cv2.imshow("Frame", clone)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q")

camera.release()
cv2.destroyAllWindows()



