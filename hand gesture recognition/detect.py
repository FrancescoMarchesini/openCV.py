from pyimagesearch.gesture_recognition.motiondetector import MotionDetector
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
(top, right, bot, left) = np.int32(args["box"].split(","))
md = MotionDetector()
numFrames = 0

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

	#altrimenti, prendo la pelle nelle roi
	else:
		#prendo il movimento dell immagine
		skin = md.detect(gray)

		#faccio il check se e stato preso il movimento
		if skin is not None:
			#update la tupla e disgno i contonri
			(thresh, c) = skin
			cv2.drawContours(clone, [c+(right, top)], -1, (0, 255, 0), 2)
			cv2.imshow("Thresh", thresh)

	#disegno un rettangolo per rappresentare la roi
	cv2.rectangle(clone, (left, top), (right, bot), (0, 0, 255), 2)
	numFrames +=1

	#mostro il frame
	cv2.imshow("Frame", clone)
	key = cv2.waitKey(1) & 0xFF

	# if the q esci
	if key == ord("q"):
		break;

	#pulisci tutto
	camera.release()
	cv2.destroyAllWindows()

