#step:
#3 Calcolare il centro di gravita (COG) della regione della mano tanto come la distanza piu grande tra il centro di gravita e il punto di lontano della mano
#-- calocola il COG

#4 costruire  un cerchi centrato nel centro di grabita che interseca tutte le dita che sono attive nella contazione
#-- Costuisci il centro e l'intetersenzione per le dita

#5 estrarre un segnale binario a 1D seguendo il center, e classificando i gesti della mano in base al numero di regioni attive (dita) nel segnale 1D
#-- estrai il segnale per determinare il numero di dita

from sklearn.metrics import pairwise
import numpy as np
import cv2
import imutils

class GestureDetector:
    def __init__(self):
        pass

    def detect(self, frame, thresh, cnt):
        #convex hull e i relativi punti piu estremi
        hull = cv2.convexHull(cnt)
        extLeft  = tuple(hull[hull[:, :, 0].argmin()][0])
        extRight = tuple(hull[hull[:, :, 0].argmax()][0])
        extTop   = tuple(hull[hull[:, :, 1].argmin()][0])
        extBot   = tuple(hull[hull[:, :, 1].argmax()][0])
        
        #tramite i punti estremi posso calcolare il centro ovvero il palmo
        cX = (extLeft[0] + extRight[0]) // 2
        cY = (extTop[1] + extBot[1]) // 2
        cY += (cY * 0.15)
        cY = int(cY)
        
        #tramite il centro posso calcolare le intersezioframe, ni
        D = pairwise.euclidean_distances([(cX, cY)], Y=[extLeft, extRight, extTop, extBot])[0]
        maxDist = D[D.argmax()]
        r = int(0.7 * maxDist)
        circum = 2 * np.pi * r

        #costruisco la ROI includendo il palmo e le dita
        circleROI = np.zeros(thresh.shape[:2], dtype="uint8")
        cv2.circle(circleROI, (cX, cY), r, (255,0, 255), 2)
        
        cv2.circle(frame, (cX, cY), 5, (255,0, 255), 2)
        cv2.circle(frame, extTop, 5, (0,0, 255), 1)
        cv2.circle(frame, extBot, 5, (0,0, 255), 1)
        cv2.circle(frame, extLeft, 5, (0,0, 255), 1)
        cv2.circle(frame, extRight, 5, (0,0, 255), 1)

        pts = np.array([extBot, extRight, extTop, extLeft], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (0, 0, 255))
        
        circleROI = cv2.bitwise_and(thresh, thresh, mask=circleROI)
        cv2.imshow("circleRoi", circleROI)

        #calcolo il numero di dita
        #il numero delle dita e' calcolato sulla ROI circolare genetata
        #in precedenza
        #CHAIN_APPROX_NONE torno il numero esatto di punti che compongo la circonferenza
        cnts = cv2.findContours(circleROI.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        total = 0;

        #loopo tra i contorni
        for (i, c) in enumerate(cnts):
            #estraggo il bounding box dei cnts
            (x, y, w, h) = cv2.boundingRect(c)

            #il dito e' calcolato come segue
            #se il numero di punti lungo il contorno non supera il 25% della circonfernza e se il contorno della circonfernza non e' alla base del dito, ovvero dove c'e il polso
            if(c.shape[0] < circum * 0.25 and ( x + y ) < cY + (cY * 0.25)):
                total += 1
                print(total)

        #ritorno il conto della dita
        return total

    #metodi statici di aiuto per visualizzare
    @staticmethod
    def drawText(roi, i , val , color=(0, 0, 255)):
            cv2.putText(roi, str(val), ((i * 50) + 20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)

    @staticmethod
    def drawBox(roi, i , color=(0, 0, 255)):
        cv2.rectangle(roi, ((i * 50) +  10, 10), ((i * 50) +  50, 60), color, 2)
