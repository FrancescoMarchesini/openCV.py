#backgorund subtraction
#step:

#1 localizza la forma che assomiglia alla mano tramite il colore della pelle estratto tramite statistiche, producendo un immagine di outpu chiamta BW
#-- localizza la mano e le dita dell'immagine

#2 fare una segmentazione della forma della mano, eliminando le piccole false regioni che sembrano una mano, tale disistinzione e fatta tramite la comporazione dei colori
#-- Elimina i falsi allarmi, ovvero le regioni che non sono le mani

import cv2
import imutils
import numpy as np

#computare la media dei pixel tra quelli passati e quelli
#attuali. Facendo poi la differnza si ha il movimento di un
#ente nello spazio
class MotionDetector:
    #maggiore e accumWight minore saranno i frame presi in considerazione
    #minore e accumWeight, maggiore sara il numero di frame per computare la media
    def __init__(self, accumWeight=0.5):
        #memorizzo l'accumulo del fattore dei pesi
        self.accumWeight = accumWeight
        #inizializzo il modello del backgroun
        self.bg = None

    def update(self, image):
        #is il background e None, inizializiamolo
        if self.bg is None:
                self.bg = image.copy().astype("float")
                return

        #update del backgorund accumulando la media dei pesi
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)
    
    def skindetect(self, image, s_l, h_l, v_l, s_h, h_h, v_h):
        #determino il range hsv nel quale cercare il colore, in questo caso il colore della pelle
        lower_hsv = np.array([s_l, h_l, v_l])
        high_hsv = np.array([s_h, h_h, v_h])

        #converto l'immagine nello spazio dei clori hsv
        convert = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #estraggo dall'immagine che pixel che cadono all'interno del range sopra determinato
        mask = cv2.inRange(convert, lower_hsv, high_hsv)

        #applico dei filtri morfologici per ottimizare la detezione della mano
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        #mask = cv2.erode(mask, kernel, iterations=1)
        #mask = cv2.dilate(mask, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        #applico un filtro gaussiano per rimuovere un po di noise
        mask = cv2.medianBlur(mask,  5)

        skin = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow("skin", skin)
        
        return mask
    
    def detect(self, image):
        #compute la differnza assuluta tra il bg model e il frame attuale
        delta = cv2.absdiff(self.bg.astype("uint8"), image)

        #trovo i contorni dell immagine
        cnts = cv2.findContours(delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        #se non c e nessun contorno ritorno none
        if len(cnts) == 0 :
                return None
        
        #altrimenti, ritorno una tupla del threshold con il contonro dell'area
        return (delta, max(cnts, key=cv2.contourArea))
